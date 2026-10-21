# StickS3 build baseline

The StickS3 software build has a measured two-run size baseline, but depends on locally provisioned inputs not packaged as a universal clean-checkout recipe.

[[docs/sticks3-build-baseline.md]] documents the tested input revisions, BMGR-before-config import order, parameterized sandbox/metadata recipe, measured static budgets, and provisioning gaps; [[docs/build-evidence/sticks3-baseline.json]] records sanitized input and result hashes. It reuses the existing ESP-IDF/BMGR workflow rather than defining a new build or deployment contract; see [[docs/epsbotik-workflow.md]].

Both independent disposable runs used candidate source revision `ce90852b919f4ed86312493f03ca3e00f69c201f`, ESP-IDF 5.5.4, StickS3/ESP32-S3, 8 MB partitioning and Octal PSRAM, and produced equal artifact sizes. The effective sdkconfig hash was `9c0d8e48c1e8239c9f42c2c8515fcc3ea2e587d25e11d15031008759b516c626`. Their binary hashes differed, so the evidence does not claim bit-identical output. The local historical lock, managed-source closure, metadata fixture, and provisioned tool environment are prerequisites outside this repository; universal reproducibility remains unestablished.

Static image and linker size output does not establish runtime heap/stack use, physical peripheral/UI behavior, or which firmware is installed on a device. No device operation is part of this baseline.
