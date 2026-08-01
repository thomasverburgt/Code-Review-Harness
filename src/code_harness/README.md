# Python Package Boundary

`code_harness` is the supported import and command-line boundary for the executable harness.

This compatibility release packages and delegates runtime behavior to the existing `tools` implementations so installed use, historical commands, and retained evidence paths remain valid. New consumers should import through `code_harness`; implementation modules will move under this package in a later GX-10-validated increment, after which `tools` will remain as temporary command wrappers.
