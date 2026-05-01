import System

open System

def main (_args : List String) : IO UInt32 := do
  IO.FS.createDirAll "tmp_lean_write_test"
  IO.FS.writeFile "tmp_lean_write_test/hello.txt" "hello\n"
  IO.println "WRITE_OK"
  return 0
