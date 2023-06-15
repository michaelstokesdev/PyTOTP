# PyTOTP

A small Python library for genertaing TOTP codes. It currently supports SHA-1, standard keys, and different length codes.

This was written over a couple of days and I recently refactored and finally uploaded it. **I would not recommend using it in a
production project**. It was mainly written to help me fully understand the TOTP standard and how it works in practice.

The library only depends on standard python libraries for math, hashing, time, and base conversion.

Testing the library against a great free [TOTP site](https://totp.danhersam.com/) by [Dan Hersam](https://github.com/jaden).

![Image of testing](/media/totp_example.png)

### Usage

The library exposes a class called ```TOTP``` which accepts arguments for the key, hashing algorithm 
(**currently not implemented, always uses the default of SHA-1**), number of digits in the outputted code (6 by default),
and the period (30 seconds by default.)

The library file also has a small builtin test function which can be used by running it directly. 

The current methods available are:

- ```generateCode(givenTime)``` - Generates a code from a given standard time value. If none is given it will use the current time.
- ```counterFromTime(givenTime, period)``` - Returns the current counter value with a given time and period value. If none are given
    it will use the current time and a 30 second period
- ```timeToNextCode(givenTime, period)``` - Returns the time to the next TOTP code. If no time or period or given they will be set to
    the current time and a 30 second period.
