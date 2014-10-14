from mycountdown import Mycountdown
import time

#def test_can_create_timer():
#    timer = Mycountdown()
    
#def test_assert_not_is_paused():
#    timer = Mycountdown()
#    assert not timer.is_paused 
    
#def test_start_timer():
#    timer = Mycountdown()
#    try:
#        timer.start_timer(0.5)
#    except Exception as e:
#        raise AssertionError(e.message)

#def test_countdown_half_second():
#    timer = Mycountdown()
#    timer.start_timer(0.0001)
#    print timer.time_left()
#    assert not timer.is_time_expired()
#    time.sleep(0.1)
#    print timer.time_left()
#    assert timer.is_time_expired()

#def test_pause_timer():
#    timer = Mycountdown()
#    timer.start_timer(0.1)
#    timer.toggle_pause_timer()
#    print timer.time_left()
#    assert timer.is_paused
#    time.sleep(1)
#    timer.toggle_pause_timer()
#    print timer.time_left()
#    assert not timer.is_paused
    
def test_time_left_beforeafter_pause():
    timer = Mycountdown()
    timer.start_timer(0.5)
    time.sleep(2)
    print timer.time_left()
    timer.toggle_pause_timer()
    time.sleep(5)
    timer.toggle_pause_timer()
    print timer.time_left()
    
    
    
