"""
Caching isn't that easy in our case.
Pip has an internal cache mechanism, which means the packages won't get downloaded for every build.
That's a good thing and already saves a lot of time. Extracting/Copying them and zipping them
afterwards still takes significant time (at least a couple seconds for everythign non-trivial) and
that's why caching is a good idea. Essentially we can merge all input requirement files and hash
the result. The result can then be used as the cache key, i.e. the

Maybe we need two staging directories
- CACHE_DIR
- BUILD_DIR

When building dependencies for a Layer these go in the build-dir. Layers only hold dependencies
and no additional application code which is why there's no point in caching these additionally.

When building lambda packages with dependencies, dependencies should be built and zipped in the
CACHE_DIR directory first. In a second step we copy the zip to the BUILD_DIR and extend it with
the application code that's passed in to the function. That way we avoid re-downloading the
dependencies all the time and only update the code that's more likely to change. It needs to be
tested, if this causes too many performance issues as I have no idea about the implications when
it comes to extending a zip. It's certainly possile with python though.

With that being said, how should a process look like?

Lambda Layers:

1. Collect requirement files and merge
2. Hash merged requirements and check if {hash}.zip is already in BUILD_DIR - if yes, return path
3. Create {hash} directory in BUILD_DIR or replace if it already exists (if that's the case a broken installation exists)
4. Create requirements.txt in {hash} directory with merged requirements
5. Create python directory in {hash} directory
6. Install requirements from requirements.txt into BUILD_DIR/{hash}/python/
7. Zip BUILD_DIR/{hash} and store as BUILD_DIR/{hash}.zip
8. Delete BUILD_DIR/{hash} directory (No longer needed)
9. Return BUILD_DIR/{hash}.zip

Lambda with dependencies:

1. Collect requirement files and merge
2. Hash merged requirements and check if {hash}.zip is already in CACHE_DIR - if yes -> Step 9
3. Create {hash} directory in CACHE_DIR or replace if it already exists (if that's the case a broken installation exists)
4. Create requirements.txt in {hash} directory with merged requirements
5. Install requirements from requirements.txt into CACHE_DIR/{hash}/python/
6. Zip CACHE_DIR/{hash} and store as CACHE_DIR/{hash}.zip
7. Delete CACHE_DIR/{hash} directory (No longer needed)
8. Hash list of Code directories -> {code_hash}
9. Copy CACHE_DIR/{hash}.zip to BUILD_DIR/{code_hash}.zip
   (otherwise we'd get problems with same dependencies and different code leading to the same deployment package)
10. Extend BUILD_DIR/{code_hash}.zip with additional code
11. Return BUILD_DIR/{code_hash}.zip
PROBLEM: Same dependencies + different code lead to same .zip!

Possible cross-platform builds could be done using docker instead of steps 4-6.
"""
