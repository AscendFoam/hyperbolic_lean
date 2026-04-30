import Lean

open Lean
open Lean.Meta

namespace DebugPreciseHierarchy

def parseName (text : String) : Name :=
  text.splitOn "." |>.foldl (init := Name.anonymous) Name.mkStr

def printDeclDebug (env : Environment) (declName : Name) : IO Unit := do
  let isStruct := isStructure env declName
  let isCls := isClass env declName
  let parentNames :=
    if isStruct then
      (getStructureParentInfo env declName).map (·.structName.toString) |>.toList
    else
      []
  let ctx : Core.Context := {
    fileName := s!"<{declName}>"
    fileMap := default
  }
  let state : Core.State := { env := env }
  let (isInst, _) ← (Meta.isInstance declName).toIO ctx state
  IO.println s!"decl={declName}"
  IO.println s!"  contains={env.contains declName}"
  IO.println s!"  isStructure={isStruct}"
  IO.println s!"  isClass={isCls}"
  IO.println s!"  isInstance={isInst}"
  IO.println s!"  parents={parentNames}"

def main (args : List String) : IO UInt32 := do
  match args with
  | mainModuleText :: decls =>
      initSearchPath (← findSysroot)
      let mainModule := parseName mainModuleText
      let env ← importModules (loadExts := true) #[{ module := mainModule }] {}
      IO.println s!"mainModule={mainModule}"
      for declText in decls do
        printDeclDebug env (parseName declText)
      return 0
  | _ =>
      IO.eprintln "usage: lake env lean --run DebugPreciseHierarchy.lean <Main.Module> <decl>..."
      return 1

end DebugPreciseHierarchy

def main (args : List String) : IO UInt32 :=
  DebugPreciseHierarchy.main args
