Running test for the first time on a fresh install will generate errors.
===

The error can safely be ignored.

    test_geoip_available (tests.test_httpfn.TestHttpFn)
    TEST: Geoip country IS avaiable ...
    ::.:! Houston?! We have a problem.

    ERROR
    test_geoip_not_available (tests.test_httpfn.TestHttpFn)
    TEST: Geoip country IS NOT available ...
    ::.:! Houston?! We have a problem.

    ERROR

The technical cause is a missing file in the folder

    tests/mock/var/status.json

The test suite is run in alphabetic order so it will be downloaded later and is available on subsequent runs.
