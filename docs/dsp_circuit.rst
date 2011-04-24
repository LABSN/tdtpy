:mod:`tdt.dsp_circuit` -- Wrapper for RPvds circuit objects
===========================================================

Error handling
--------------

Attempting to get/set the value of a nonexistent tag in the circuit will raise a
`DSPError`:

>>> circuit.get_tag('nonexistent_tag')
DSPError: 'nonexistent_tag' not found in circuit

