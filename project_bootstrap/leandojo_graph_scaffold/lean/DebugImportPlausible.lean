import Lean
import Plausible

open Lean
open Lean.Meta

def main (_args : List String) : IO UInt32 := do
  let env ← importModules (loadExts := true) #[{ module := `Plausible }] {}
  let ctx : Core.Context := {
    fileName := "<DebugImportPlausible>"
    fileMap := default
  }
  let state : Core.State := { env := env }

  let dump (declName : Name) : IO Unit := do
    let (isInst, _) ← (Meta.isInstance declName).toIO ctx state
    IO.println s!"decl={declName}"
    IO.println s!"  contains={env.contains declName}"
    IO.println s!"  isStructure={isStructure env declName}"
    IO.println s!"  isClass={isClass env declName}"
    IO.println s!"  isInstance={isInst}"

  dump `Plausible.Shrinkable
  dump `Plausible.SampleableExt
  dump `Plausible.Unit.shrinkable
  dump `Plausible.Random
  dump `Plausible.Configuration
  return 0
