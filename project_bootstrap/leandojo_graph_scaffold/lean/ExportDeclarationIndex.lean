import Lean

open Lean
open System

namespace DeclarationIndexExport

structure DeclIndexRow where
  declName : Name
  declKind : String
  moduleName : String
  lineStart : Nat
  lineEnd : Nat
  selectionLineStart : Nat
  selectionLineEnd : Nat

def parseName (text : String) : Name :=
  text.splitOn "." |>.foldl (init := Name.anonymous) Name.mkStr

def shortDeclNameText (declName : Name) : String :=
  declName.toString.splitOn "." |>.getLastD declName.toString

def tsvLine (fields : List String) : String :=
  "\t".intercalate fields

def collectConstantNames (env : Environment) : Array Name :=
  (env.constants.fold (fun names name _ => names.push name) #[]).qsort Name.quickLt

def getModuleContainingDecl? (env : Environment) (declName : Name) : Option Name :=
  match env.getModuleIdxFor? declName with
  | some modIdx => env.allImportedModuleNames.get? modIdx
  | none =>
      if env.contains declName then
        some env.mainModule
      else
        none

def inferDeclKind (env : Environment) (declName : Name) : CoreM String := do
  if (← Lean.Meta.isInstance declName) then
    return "instance"
  if isClass env declName then
    return "class"
  if isStructure env declName then
    return "structure"
  match env.find? declName with
  | some (.thmInfo _) => return "theorem"
  | some (.defnInfo _) => return "def"
  | some (.opaqueInfo _) => return "opaque"
  | some (.axiomInfo _) => return "axiom"
  | some (.inductInfo _) => return "inductive"
  | some (.ctorInfo _) => return "constructor"
  | some (.recInfo _) => return "recursor"
  | some (.quotInfo _) => return "quot"
  | none => return "unknown"

def collectRows : CoreM (Array DeclIndexRow) := do
  let env ← getEnv
  let mut rows : Array DeclIndexRow := #[]
  for declName in collectConstantNames env do
    let some ranges ← findDeclarationRanges? declName | continue
    let declKind ← inferDeclKind env declName
    let moduleName := (getModuleContainingDecl? env declName).map Name.toString |>.getD ""
    rows := rows.push {
      declName := declName
      declKind := declKind
      moduleName := moduleName
      lineStart := ranges.range.pos.line
      lineEnd := ranges.range.endPos.line
      selectionLineStart := ranges.selectionRange.pos.line
      selectionLineEnd := ranges.selectionRange.endPos.line
    }
  return rows.qsort (fun a b => Name.quickLt a.declName b.declName)

def writeRows (path : FilePath) (rows : Array DeclIndexRow) : IO Unit := do
  let mut lines := #[
    tsvLine [
      "decl_name",
      "decl_short_name",
      "decl_kind",
      "module_name",
      "line_start",
      "line_end",
      "selection_line_start",
      "selection_line_end",
    ]
  ]
  for row in rows do
    lines := lines.push <| tsvLine [
      row.declName.toString,
      shortDeclNameText row.declName,
      row.declKind,
      row.moduleName,
      toString row.lineStart,
      toString row.lineEnd,
      toString row.selectionLineStart,
      toString row.selectionLineEnd,
    ]
  IO.FS.writeFile path <| String.intercalate "\n" lines.toList ++ "\n"

def usage : String :=
  "usage: lake env lean --run ExportDeclarationIndex.lean <Main.Module> <output-tsv>"

def main (args : List String) : IO UInt32 := do
  match args with
  | mainModuleText :: outputPathText :: _ => do
      initSearchPath (← findSysroot)
      let mainModule := parseName mainModuleText
      let env ← importModules (loadExts := true) #[{ module := mainModule }] {}
      let ctx : Core.Context := {
        fileName := s!"<{mainModuleText}>"
        fileMap := default
      }
      let state : Core.State := { env := env }
      let (rows, _) ← (collectRows).toIO ctx state
      let outputPath := FilePath.mk outputPathText
      IO.FS.createDirAll (outputPath.parent.getD (FilePath.mk "."))
      writeRows outputPath rows
      IO.println s!"[done] declaration rows: {rows.size}"
      IO.println s!"[done] output: {outputPath}"
      return 0
  | _ => do
      IO.eprintln usage
      return 1

end DeclarationIndexExport

def main (args : List String) : IO UInt32 :=
  DeclarationIndexExport.main args
