"""
We entangle two qbits and put them in the Bell state.
After the entanglement, the measurement of the two qbits
shour always agree to each other.
"""
from quantum import *


def show():
    system = get_system()
    # Create a quantum system. Note that this system is global
    # # so calling it multiple times only returns the same object
    with system.register(2) as (q1, q2):
        print("Initial state:\n", system)
        H(q1)             # Apply Harmard gate to q1
        print("Apply Harmard gate to q1:\n", system)
        CNot(q1, q2)      # Apply controlled-not gate to q1, q2
        print("CNot(q1, q2):\n", system)
        # Now the state of the system if sqrt(0.5) * (|00> + |11>),
        # the two qbits are entangled
        Measure(q1)
        print("Measure(q1):\n", system)
        ResetAll([q1, q2])  # Reset the qubits after using them


def experiment(n):
    system = get_system()
    agreed = 0
    for _ in range(n):
        with system.register(2) as (q1, q2):
            H(q1)             # Apply Harmard gate to q1
            CNot(q1, q2)      # Apply controlled-not gate to q1, q2
            state1 = Measure(q1)
            state2 = Measure(q2)
            if state1 == state2:
                agreed += 1
            ResetAll([q1, q2])  # Reset the qubits after using them
    return agreed


def main():
    print("After the entanglement the measurement of the two qbits should agree to"
          "each other.")
    n = 50
    agreed = experiment(n)
    print("Agreed: {} / {}".format(agreed, n))

    print("Now we show the state of the system of the different states:")
    show()
    

if __name__ == '__main__':
    main()
