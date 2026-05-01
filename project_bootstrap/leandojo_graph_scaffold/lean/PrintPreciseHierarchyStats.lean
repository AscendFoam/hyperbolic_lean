import Lean

open Lean
open Lean.Meta

namespace PrintPreciseHierarchyStats

def parseName (text : String) : Name :=
  text.splitOn "." |>.foldl (init := Name.anonymous) Name.mkStr

def collectConstantNames (env : Environment) : Array Name :=
  (env.constants.fold (fun names name _ => names.push name) #[]).qsort Name.quickLt

def inferInstanceTarget? (declName : Name) : CoreM (Option Name) := do
  let env <- getEnv
  let info <- getConstInfo declName
  MetaM.run' do
    forallTelescopeReducing info.type fun _ targetType => do
      withReducible do
        let targetType <- whnf targetType
        match targetType.getAppFn with
        | Expr.const className _ =>
            if isClass env className then
              return some className
            else
              return none
        | _ =>
            return none

structure HierarchyStats where
  structureCount : Nat
  classCount : Nat
  instanceCount : Nat
  extendsCount : Nat
  instanceOfCount : Nat

def collectStats : CoreM HierarchyStats := do
  let env <- getEnv
  let mut structureCount := 0
  let mut classCount := 0
  let mut instanceCount := 0
  let mut extendsCount := 0
  let mut instanceOfCount := 0

  for declName in collectConstantNames env do
    let structInfo? := getStructureInfo? env declName
    let isStructureDecl := structInfo?.isSome
    let isClassDecl := isClass env declName
    let isInstanceDecl <- Meta.isInstance declName

    if isStructureDecl then
      structureCount := structureCount + 1
      if let some structInfo := structInfo? then
        extendsCount := extendsCount + structInfo.parentInfo.size

    if isClassDecl then
      classCount := classCount + 1

    if isInstanceDecl then
      instanceCount := instanceCount + 1
      let instanceTarget? <- inferInstanceTarget? declName
      if instanceTarget?.isSome then
        instanceOfCount := instanceOfCount + 1

  return {
    structureCount := structureCount
    classCount := classCount
    instanceCount := instanceCount
    extendsCount := extendsCount
    instanceOfCount := instanceOfCount
  }

def usage : String :=
  "usage: lake env lean --run PrintPreciseHierarchyStats.lean <Main.Module>"

def main (args : List String) : IO UInt32 := do
  match args with
  | mainModuleText :: _ => do
      initSearchPath (← findSysroot)
      let mainModule := parseName mainModuleText
      let env <- importModules (loadExts := true) #[{ module := mainModule }] {}
      let ctx : Core.Context := {
        fileName := s!"<{mainModuleText}>"
        fileMap := default
      }
      let state : Core.State := { env := env }
      let (stats, _) <- collectStats.toIO ctx state
      IO.println s!"[stats] structures={stats.structureCount}"
      IO.println s!"[stats] classes={stats.classCount}"
      IO.println s!"[stats] instances={stats.instanceCount}"
      IO.println s!"[stats] exact_extends={stats.extendsCount}"
      IO.println s!"[stats] exact_instance_of={stats.instanceOfCount}"
      return 0
  | _ => do
      IO.eprintln usage
      return 1

end PrintPreciseHierarchyStats

def main (args : List String) : IO UInt32 :=
  PrintPreciseHierarchyStats.main args
