import Lean

open Lean
open Lean.Meta
open System

namespace PreciseHierarchyExport

structure NodeRow where
  declName : Name
  isStructure : Bool
  isClass : Bool
  isInstance : Bool
  parentCount : Nat
  instanceTarget? : Option Name := none

structure RelationRow where
  srcName : Name
  dstName : Name
  relationType : String
  evidenceSource : String := "lean_meta_exact"

def parseName (text : String) : Name :=
  text.splitOn "." |>.foldl (init := Name.anonymous) Name.mkStr

def boolText (flag : Bool) : String :=
  if flag then "true" else "false"

def tsvLine (fields : List String) : String :=
  "\t".intercalate fields

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

structure HierarchyRows where
  nodeRows : Array NodeRow
  relationRows : Array RelationRow

def collectRows : CoreM HierarchyRows := do
  let env <- getEnv
  let mut nodeRows : Array NodeRow := #[]
  let mut relationRows : Array RelationRow := #[]

  for declName in collectConstantNames env do
    let structInfo? := getStructureInfo? env declName
    let isStructure := structInfo?.isSome
    let isClassDecl := isClass env declName
    let isInstanceDecl <- Meta.isInstance declName
    let parents :=
      if let some structInfo := structInfo? then
        structInfo.parentInfo.map (fun (parentInfo : Lean.StructureParentInfo) => parentInfo.structName)
      else
        #[]
    let instanceTarget? <-
      if isInstanceDecl then
        inferInstanceTarget? declName
      else
        pure none

    if isStructure || isInstanceDecl then
      nodeRows := nodeRows.push {
        declName := declName
        isStructure := isStructure
        isClass := isClassDecl
        isInstance := isInstanceDecl
        parentCount := parents.size
        instanceTarget? := instanceTarget?
      }

    for parentName in parents do
      relationRows := relationRows.push {
        srcName := declName
        dstName := parentName
        relationType := "extends"
      }

    if let some className := instanceTarget? then
      relationRows := relationRows.push {
        srcName := declName
        dstName := className
        relationType := "instance_of"
      }

  return {
    nodeRows := nodeRows
    relationRows := relationRows
  }

def writeNodeRows (path : FilePath) (rows : Array NodeRow) : IO Unit := do
  let mut lines := #[tsvLine [
    "decl_name",
    "is_structure",
    "is_class",
    "is_instance",
    "parent_count",
    "instance_target",
  ]]
  for row in rows do
    lines := lines.push <| tsvLine [
      row.declName.toString,
      boolText row.isStructure,
      boolText row.isClass,
      boolText row.isInstance,
      toString row.parentCount,
      row.instanceTarget?.map Name.toString |>.getD "",
    ]
  IO.FS.writeFile path <| String.intercalate "\n" lines.toList ++ "\n"

def writeRelationRows (path : FilePath) (rows : Array RelationRow) : IO Unit := do
  let mut lines := #[tsvLine [
    "src_name",
    "dst_name",
    "relation_type",
    "evidence_source",
  ]]
  for row in rows do
    lines := lines.push <| tsvLine [
      row.srcName.toString,
      row.dstName.toString,
      row.relationType,
      row.evidenceSource,
    ]
  IO.FS.writeFile path <| String.intercalate "\n" lines.toList ++ "\n"

def usage : String :=
  "usage: lake env lean --run ExportPreciseHierarchy.lean <Main.Module> <output-dir>"

def main (args : List String) : IO UInt32 := do
  match args with
  | mainModuleText :: outputDirText :: _ => do
      initSearchPath (← findSysroot)
      let mainModule := parseName mainModuleText
      let outputDir := FilePath.mk outputDirText
      let env <- importModules (loadExts := true) #[{ module := mainModule }] {}
      let ctx : Core.Context := {
        fileName := s!"<{mainModuleText}>"
        fileMap := default
      }
      let state : Core.State := { env := env }
      let (rows, _) <- collectRows.toIO ctx state
      IO.FS.createDirAll outputDir
      writeNodeRows (outputDir / "nodes.tsv") rows.nodeRows
      writeRelationRows (outputDir / "relations.tsv") rows.relationRows
      IO.println s!"[done] nodes: {rows.nodeRows.size}"
      IO.println s!"[done] relations: {rows.relationRows.size}"
      IO.println s!"[done] output: {outputDir}"
      return 0
  | _ => do
      IO.eprintln usage
      return 1

end PreciseHierarchyExport

def main (args : List String) : IO UInt32 :=
  PreciseHierarchyExport.main args
