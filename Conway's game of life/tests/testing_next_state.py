import sys
sys.path.append('../src')
from life import next_board_state

def test(actual, expected):
    if expected == actual:
        print ("PASSED")
    else:
        print ("FAILED!")
        print ("Expected:")
        print (expected)
        print ("Actual:")
        print (actual)

if __name__ == "__main__":
    # TEST 1: dead cells with no live neighbors
    # should stay dead.
    init_state1 = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    expected_next_state1 = [
        [0,0,0],
        [0,0,0],
        [0,0,0]
    ]
    actual_next_state1 = next_board_state(init_state1)
    test(actual_next_state1, expected_next_state1)


    # TEST 2: dead cells with exactly 3 neighbors
    # should come alive.
    init_state2 = [
        [0,0,1],
        [0,1,1],
        [0,0,0]
    ]
    expected_next_state2 = [
        [0,1,1],
        [0,1,1],
        [0,0,0]
    ]
    actual_next_state2 = next_board_state(init_state2)
    test(actual_next_state2, expected_next_state2)
    
    # TEST 3: Alive cells with more than 3 neighbours should become dead
    init_state3 = [
        [1,1,1],
        [0,1,1],
        [0,0,0]
    ]
    expected_next_state3 = [
        [1,0,1],
        [1,0,1],
        [0,0,0]
    ]
    actual_next_state3 = next_board_state(init_state3)
    test(actual_next_state3, expected_next_state3)