import System

open System

def main (_args : List String) : IO UInt32 := do
  let outPath : FilePath := "/mnt/d/Codes/Math/hyperbolic_lean/artifacts/logs/smoke_exit_123.txt"
  IO.FS.createDirAll (outPath.parent.getD (FilePath.mk "."))
  IO.FS.writeFile outPath "smoke-ok\n"
  return 123
