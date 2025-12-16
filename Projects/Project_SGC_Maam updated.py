import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Robot:
    def __init__(self, x, y, name=None):
        # Here the robot see it's coordinate
        self.x = x
        self.y = y
        # self.last_move = None   # track last direction: "west", "east", or None
        self.name = name if name else f"R({x},{y})"

    def position(self):
        return (self.x, self.y)

    def move(self, dx, dy,flag):
        self.x += dx
        self.y += dy

        # Show movement before updating (help me to see the flow)
        
        # if(flag == 3 ): print(f"Case 3: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 3.6 ): print(f"Case 3.6: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 3.4 ): print(f"Case 3.4: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 4 ): print(f"Case 4: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 5 ): print(f"Case 5: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 6 ): print(f"{self} Case 6: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 1 ): print(f"Case 1: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")
        # if(flag == 2 ): print(f"Case 2: ({self.x},{self.y}) -> ({self.x + dx},{self.y + dy})", end=" ")

        
    # Not so much Important / Essential. It just name the robot base on it's coordinate
    def __repr__(self):
        return f"{self.name}@({self.x},{self.y})"


# This will run for all the robots to set their position
class GridScatter:
    def __init__(self, robots):
        self.robots = robots
    
    # It checks that all the robots are in alternative position or not. If yes then it return True
    def check_x_gap(self):  
        rows = {}
        for r in self.robots:
            rows.setdefault(r.y, []).append(r.x)

        for xs in rows.values():
            xs.sort()
            for i in range(1, len(xs)):
                if xs[i] - xs[i-1] != 2:
                    return False
        return True
    
    # It checks that all the robots (at specific row) are in alternative position or not. If yes then it return True
    def check_x_gap_at_r(self, robot, XMIN): 
        xs = [r.x for r in self.robots if r.y == robot.y]
        # check gaps
        xs.sort()
        if len(xs) == 1 and xs != XMIN:
            return False
        for i in range(1, len(xs)):
            if xs[i] - xs[i-1] != 2:
                return False
        # print("True ",robot,end=" ")
        return True

    # It checks whether the robot itself is capable of moving west
    ''' Criteria: 1. If all the robots (except the current) are in alternative Position
                  2. The westmost robot belongs to the XMIN '''
    def is_West_Move_Capable(self, robot, XMIN): 
        xs = [r.x for r in self.robots if r.y == robot.y and r.x < robot.x]
        xs.sort()

        for i in range(1, len(xs)): # Checking for alternative position
            if xs[i] - xs[i-1] != 2:
                return False   
             
        westmost_robot_x = [r.x for r in self.robots if r.y == robot.y and r.x < robot.x]
        westmost_robot_x.sort()
        if westmost_robot_x[0] != XMIN: # Check that the westmost robot belongs to XMIN or Not
            return False
        
        return True

    # It checks whether the neighbor's robot is able to move west or not. If yes, then the current robot Will not move
    def neighbour_robot_can_move(self, robot, XMIN):
        xs = [r.x for r in self.robots if r.y == robot.y and r.x < robot.x]
        # check gaps
        xs.sort()
        for neighbour_robot_x in xs:
            if neighbour_robot_x == XMIN:
                continue  # This neighbor is at the boundary, skip
            # Try west move
            if not self.occupied(neighbour_robot_x - 1, robot.y) and not self.occupied(neighbour_robot_x - 2, robot.y):
                return True
            # Try east move
            if not self.occupied(neighbour_robot_x + 1, robot.y) and not self.occupied(neighbour_robot_x + 2, robot.y):
                return True
        return False

    # It checks whether there is any space left above (means in the odd row) or not.
    def has_free_space_above(self, x, y, YMAX):
        """
        Check if there is any free space above robot at (x, y).
        Free space = no robot at (x, y') for some y' > y
        """
        # Loop through all rows above current robot
        for y_above in range(y + 2, YMAX + 1):
            # Check if a robot already exists at (x, y_above)
            is_all_occupied = all(r.x == x and r.y == y_above for r in self.robots)
            if not is_all_occupied:  # found a gap above
                return True
        return False

    # It checks whether all the robots are uniformly distributed or not. It is basically a self-check to prevent infinite loops
    def is_Uniformly_Distributed(self, rc, YMAX, XMIN, dimension):
        # Group robots by row (y-coordinate)
        rows = {}
        for r in self.robots:
            rows.setdefault(YMAX - r.y + 1, []).append(r.x)
        # Sort y descending (top → bottom)
        sorted_rows = sorted(rows.keys(), reverse=True)
        if max(sorted_rows) > dimension: return False

        # Checking that there is any upper row has less robot than the lower row (base on actual y-axis of hte robot not Ymax)
        for i in range(1, len(sorted_rows)):
            upper = sorted_rows[i - 1]   # higher (top) row
            lower = sorted_rows[i]       # lower (bottom) row
            if len(rows[upper]) > len(rows[lower]):
                return False
            
        # Checking that there is any upper row has same robot than the lower row (base on actual y-axis of hte robot not Ymax)
        for i in range(1, len(sorted_rows)):
            upper = sorted_rows[i - 1]   # higher (top) row
            lower = sorted_rows[i]       # lower (bottom) row
            if len(rows[upper]) == len(rows[lower]) < rc:
                return False

        # Other Flags/Checker    
        for y in sorted_rows:
            if y % 2 == 0:
                return False
            if y % 2 == 1 and len(rows[y]) > rc:
                return False
            
            if rows[y] and min(rows[y]) != XMIN:
                return False
        
            if y == dimension and max(rows[y]) == dimension - 1:
                j = YMAX - dimension + 1
                target_robot = next((r for r in self.robots if r.x == dimension-1 and r.y == j), None)
                if target_robot and not self.check_x_gap_at_r(target_robot, XMIN):
                    return not self.has_free_space_above(dimension - 1, j, YMAX)

            for xs in rows.values():
                xs.sort()
                for i in range(1, len(xs)):
                    if xs[i] - xs[i-1] != 2:
                        return False
                    
        # Check total number of robots matches
        if len(self.robots) != sum(len(rows[y]) for y in rows):
            return False
        return True

    def occupied(self, x, y): # check the place is occupied or free
        return any(r.x == x and r.y == y for r in self.robots)

    def find_dimension(self): # It is used to find the dimension and maximum number of robots in a row. It is basically Algorithm 1 (FindDimension())
        n = len(self.robots)
        rc = math.ceil(math.sqrt(n))        # max robots in row
        d = (rc * 2) - 1                    # max rows
        return rc, d

    def find_YMAX(self): # Algorithm 2 (FindYMAX())
        return max(r.y for r in self.robots)

    def find_XMIN(self): # Algorithm 3 (FindXMIN())
        return min(r.x for r in self.robots)

    # It checks whether the current robot is the westmost robot or not   
    def is_westmost(self, r, XMIN):
        for other in self.robots:
            if other.y == r.y and other.x < r.x:  # someone is further west
                return False
        return True

    # It mainly ensures that case 1 and case 2 are fully satisfied
    def is_case1_case2_completed(self, YMAX):
        for other in self.robots:
            j = YMAX - other.y + 1
            if j % 2 == 0:
                return False
            
        return True
  
    # Check if robot r is in its correct final position using d (rows) and rc (columns).
    def is_in_correct_position(self, r, XMIN, YMAX, d, rc):

        # Row index (1 = top row)
        j = YMAX - r.y + 1

        # --- Row check ---
        if j > d:              # beyond distribution depth
            return False
        if j % 2 == 0:          # must be odd row
            return False

        count = sum(1 for other in self.robots if other.y == r.y and other.x <= r.x) # how many robots are before me

        temp_dimension = round(d/2)
        if r.x > (XMIN + temp_dimension):
            return False
        if self.occupied(r.x-1,r.y) and ((r.x-1) - XMIN) % 2 == 1:
            return False
        if (r.x - XMIN) % 2 != 0: # Check if the robots are in an even column or not. If no, then it is not in the correct position
            return False
        if r.x - 2 == XMIN and not self.occupied(r.x - 2, r.y):
            return False
        if not self.check_x_gap_at_r(r, XMIN):
            return False

        return True

    # It counts the number of robots present above me
    def count_robots_above(self, x, y):
        count = sum(1 for r in self.robots if r.y == y + 2)
        count_r = [r for r in self.robots if r.y == y + 2]
        print("count ",count_r, y)
        return count
    
    def form_grid(self, steps=1000): # Algorithm 4 (FormGrid())
        rc, d = self.find_dimension()
        YMAX = self.find_YMAX()
        XMIN = self.find_XMIN()
        # XMAX = 2 * rc -2 
        number_of_iteration = 0

        # ### NEW: Create a list to store the history of positions
        history = []
        # Store the initial state
        history.append([(r.x, r.y) for r in self.robots]) 
        # ###
        
        for step in range(steps):
        # while not self.is_Uniformly_Distributed(rc, YMAX, XMIN, d):  # Self-checking 
            moved = False
            number_of_iteration += 1
            # ordered_robots = sorted(self.robots, key=lambda r: (-r.y, r.x))
            for r in self.robots:
                j = YMAX - r.y + 1   # row index (1 = top row)

                # --- Priority Order ---
                # For Case 1 and 2 : upper > west > east > south > north
                # For remaining cases: west > east > south > north
                priority = {"upper": 0, "west": 1, "east": 2, "south": 3, "north": 4, "wait": 5, "north_east": 6}
                potential_moves = []

                # --- Case Ψ1: Even row within d rows --- ==> Outcome: Even row's robot moves to Odd rows <==
                if j <= d and j % 2 == 0:
                    if not self.occupied(r.x, r.y+1):
                        # r.move(0, 1)
                        potential_moves.append(("upper", (0, 1, 1)))
                        j = j - 1
                        moved=True
                    elif not self.occupied(r.x+1, r.y):
                        # r.move(1, 0)
                        potential_moves.append(("upper", (1, 0, 1)))
                        moved=True
                    else:
                        pass # Robot r waits

                # --- Case Ψ2: Beyond d rows ---  ==> Outcome: Even rows' robot that present outside the boundary (j > d) moves to odd rows () <==
                elif j > d:
                    if not self.occupied(r.x, r.y+1):
                        # r.move(0, 1)
                        potential_moves.append(("upper", (0, 1, 2)))
                        j = j - 1
                        moved=True
                    elif not self.occupied(r.x+1, r.y):
                        # r.move(1, 0)
                        potential_moves.append(("upper", (1, 0, 2)))
                        moved=True
                    else:
                        pass # Robot r waits

                # --- Case Ψ3: Odd row but not alternate node --- ==> Outcome: All odd rows' robots go to alternative positions in a row <==
                if j % 2 == 1 and r.x != XMIN and self.is_case1_case2_completed(YMAX) and not self.is_in_correct_position(r, XMIN, YMAX, d, rc): 

                    if self.is_westmost(r, XMIN): # The roborts present near to XMIN goes to XMIN
                        if r.x - 1 >= XMIN and not self.occupied(r.x-1, r.y):
                            potential_moves.append(("west", (-1, 0,3.4)))
                            moved = True  

                    # If two west cells are free, move west
                    elif r.x - 2 >= XMIN  and self.is_West_Move_Capable(r,XMIN) and not self.occupied(r.x-1, r.y) and not self.occupied(r.x-2, r.y): 
                        potential_moves.append(("west", (-1, 0, 3)))
                        moved=True

                    # if the west cells are not free and the robot is not in XMIN
                    elif  r.x != XMIN and not self.neighbour_robot_can_move(r, XMIN): # r.last_move != "west" and # and not self.is_in_correct_position(r, XMIN, YMAX, d, rc)
                        # Else, if two east cells are free, move east
                        if not self.check_x_gap_at_r(r, XMIN) and not self.occupied(r.x+1, r.y) and not self.occupied(r.x+2, r.y): 
                            potential_moves.append(("east", (1, 0, 3.6)))
                            moved=True  
                    
                    # This is the exceptional case where the NxN position robot can move to east though it moves to west
                    # elif r.x != XMIN and r.x == max(rob.x for rob in self.robots if rob.y == r.y) and not self.check_x_gap_at_r(r, XMIN) and not self.occupied(r.x+1, r.y) and not self.occupied(r.x+2, r.y) and self.occupied(r.x-2,r.y) and (r.x-2)%2 != 0: # and r.last_move == "west"
                    #     potential_moves.append(("east", (1, 0,3.5)))
                    #     moved=True 

                    else:
                        pass # Robot r waits

                # --- Case Ψ4: First rc robots in row move northwards --- ==> Outcome: First rc robots in row move to North <==
                if j % 2 == 1 and self.is_case1_case2_completed(YMAX) and self.check_x_gap(): # check_x_gap() ==> it checks that all the robots are in alternative position or not
                    row_robots = sorted([r2 for r2 in self.robots if r2.y == r.y], key=lambda r2: r2.x) # Get robots in this row sorted by x (west → east)
                    # Check if this robot is in the first rc robots
                    if r in row_robots[:rc]:
                        # print(r,end=" ")
                        if j != 1 and not self.occupied(r.x, r.y+2):
                            potential_moves.append(("north", (0, 2, 4)))   # move north
                            moved = True
                            j = j - 2   # this is implicit because next loop recomputes j
                    
                # --- Case Ψ5: Excess robots in a row --- ==> Outcome: Extra robots gets their position <==
                if j % 2 == 1 and self.check_x_gap(): # check_x_gap() ==> it checks that all the robots are in alternative position or not
                    west_count = sum(1 for r2 in self.robots if r2.y == r.y and r2.x < r.x)
                    if west_count >= rc:  # only excess robots move
                        # ---- Case A: bottom row j == 1 ----
                        if j == 1:
                            if not self.occupied(r.x, r.y-2):  # try move south
                                # r.move(0, -2)
                                potential_moves.append(("south", (0, -2, 5)))
                                moved = True
                            else:
                                pass  # wait until (x,y-2) is free

                            # if fewer than rc west robots, try sliding west
                            if west_count < rc and r.x - 2 >= XMIN and \
                            not self.occupied(r.x-1, r.y) and not self.occupied(r.x-2, r.y):
                                # r.move(-1, 0)
                                
                                potential_moves.append(("west", (-1, 0, 5)))
                                moved = True

                        # ---- Case B: higher rows j > 1 ----
                        else:
                            # Count robots in odd rows above
                            odd_above = [r2 for r2 in self.robots if r2.y > r.y and (YMAX - r2.y + 1) % 2 == 1]
                            if len(odd_above) < rc:
                                # move north
                                if not self.occupied(r.x, r.y+2):
                                    # r.move(0, 2)
                                    potential_moves.append(("north", (0, 2, 5)))
                                    moved = True
                            else:
                                # move south
                                if not self.occupied(r.x, r.y-2):
                                    # r.move(0, -2)
                                    potential_moves.append(("south", (0, -2, 5)))
                                    moved = True

                            # westward adjustment if fewer than rc robots on west
                            if west_count < rc and r.x - 2 >= XMIN and \
                            not self.occupied(r.x-1, r.y) and not self.occupied(r.x-2, r.y):
                                # r.move(-1, 0)
                                potential_moves.append(("west", (-1, 0, 5)))
                                moved = True
                                    
                if potential_moves: # It is a tie breaking that works on priority
                        # Pick move with smallest priority rank
                        best = min(potential_moves, key=lambda m: priority[m[0]])
                        (dx, dy,f) = best[1]
                        r.move(dx,dy,f)
                        # r.move(dx,dy)

            # ### NEW: Capture the state at the end of the iteration
            history.append([(r.x, r.y) for r in self.robots])
            # ###

            if not moved:
                break  # no more moves → stable
    
        return number_of_iteration,history

    def display(self): # To show the Output
        coords = {r.position(): r.name for r in self.robots}

        xs = [r.x for r in self.robots]
        ys = [r.y for r in self.robots]
        for y in range(max(ys), 0, -1): #for y in range(max(ys), min(ys)-1, -1):
            row = ""
            for x in range(min(xs), max(xs)+1): # min(xs)
                if (x,y) in coords:
                    row += "R "
                else:
                    row += ". "
            print(row)

    # def visualize_robots(self, history, x_min, x_max, y_min, y_max):
    #     import matplotlib.pyplot as plt
    #     from matplotlib.widgets import Button
    #     import numpy as np

    #     # --- Setup the Figure ---
    #     fig, ax = plt.subplots(figsize=(8, 9))
    #     plt.subplots_adjust(bottom=0.2) # Make space at bottom for buttons

    #     # Dictionary to keep track of current frame and playing status
    #     state = {
    #         'index': 0, 
    #         'playing': False
    #     }

    #     # --- Drawing Function ---
    #     def draw_frame(i):
    #         ax.clear()
            
    #         # Grid Settings
    #         ax.set_title(f"Iteration: {i} / {len(history)-1}")
    #         ax.set_xlim(x_min - 1, x_max + 1)
    #         ax.set_ylim(y_min - 1, y_max + 1)
    #         ax.set_aspect('equal')
            
    #         # Grid Lines
    #         y_ticks = np.arange(int(y_min), int(y_max) + 2, 1)
    #         x_ticks = np.arange(int(x_min), int(x_max) + 2, 1)
    #         ax.set_yticks(y_ticks)
    #         ax.set_xticks(x_ticks)
    #         ax.grid(True, which='both', linestyle='--', linewidth=1, color='gray', alpha=0.5)

    #         # Draw Robots
    #         positions = history[i]
    #         robot_marker = "🤖" 
            
    #         for pos in positions:
    #             try:
    #                 ax.text(pos[0], pos[1], robot_marker, 
    #                         horizontalalignment='center', verticalalignment='center', 
    #                         fontsize=20, fontname='Segoe UI Emoji', color='blue', zorder=3)
    #             except:
    #                 ax.text(pos[0], pos[1], "R", 
    #                         horizontalalignment='center', verticalalignment='center', 
    #                         fontsize=14, fontweight='bold', color='blue', zorder=3)
    #         plt.draw()

    #     # --- Button Logic ---
    #     def next_step(event):
    #         if state['index'] < len(history) - 1:
    #             state['index'] += 1
    #             draw_frame(state['index'])
    #         elif state['playing']: 
    #             # If playing and reached the end, stop automatically
    #             toggle_play(None)

    #     def prev_step(event):
    #         if state['index'] > 0:
    #             state['index'] -= 1
    #             draw_frame(state['index'])

    #     # --- Timer Logic for Auto-Play ---
    #     # Interval=800 means 0.8 seconds per step. Change to 500 for faster, 1000 for slower.
    #     timer = fig.canvas.new_timer(interval=800) 
    #     timer.add_callback(next_step, None)

    #     def toggle_play(event):
    #         if state['playing']:
    #             # STOP
    #             timer.stop()
    #             state['playing'] = False
    #             bplay.label.set_text("Play")
    #         else:
    #             # START
    #             # If we are already at the end, restart from 0
    #             if state['index'] >= len(history) - 1:
    #                 state['index'] = 0
    #                 draw_frame(0)
                
    #             timer.start()
    #             state['playing'] = True
    #             bplay.label.set_text("Pause")
        
    #     # --- Keyboard Support ---
    #     def on_key(event):
    #         if event.key == 'right': next_step(None)
    #         elif event.key == 'left': prev_step(None)
    #         elif event.key == ' ' or event.key == 'enter': toggle_play(None)

    #     # --- Create Buttons [left, bottom, width, height] ---
    #     axprev = plt.axes([0.15, 0.05, 0.2, 0.075])
    #     axplay = plt.axes([0.40, 0.05, 0.2, 0.075]) # Middle button
    #     axnext = plt.axes([0.65, 0.05, 0.2, 0.075])
        
    #     bprev = Button(axprev, 'Previous')
    #     bplay = Button(axplay, 'Play')
    #     bnext = Button(axnext, 'Next')
        
    #     bprev.on_clicked(prev_step)
    #     bplay.on_clicked(toggle_play)
    #     bnext.on_clicked(next_step)
        
    #     fig.canvas.mpl_connect('key_press_event', on_key)

    #     # Initial Draw
    #     draw_frame(0)
    #     plt.show()




    def visualize_robots(self, history, x_min, x_max, y_min, y_max):
        import matplotlib.pyplot as plt
        from matplotlib.widgets import Button
        from matplotlib.animation import PillowWriter # --- NEW IMPORT ---
        import numpy as np

        # --- Setup the Figure ---
        fig, ax = plt.subplots(figsize=(8, 9))
        plt.subplots_adjust(bottom=0.2) # Make space at bottom for buttons

        # Dictionary to keep track of current frame and playing status
        state = {
            'index': 0, 
            'playing': False
        }

        # --- Drawing Function ---
        def draw_frame(i):
            ax.clear()
            
            # Grid Settings
            ax.set_title(f"Iteration: {i} / {len(history)-1}")
            ax.set_xlim(x_min - 1, x_max + 1)
            ax.set_ylim(y_min - 1, y_max + 1)
            ax.set_aspect('equal')
            
            # Grid Lines
            y_ticks = np.arange(int(y_min), int(y_max) + 2, 1)
            x_ticks = np.arange(int(x_min), int(x_max) + 2, 1)
            ax.set_yticks(y_ticks)
            ax.set_xticks(x_ticks)
            ax.grid(True, which='both', linestyle='--', linewidth=1, color='gray', alpha=0.5)

            # Draw Robots
            positions = history[i]
            robot_marker = "🤖" 
            
            for pos in positions:
                try:
                    ax.text(pos[0], pos[1], robot_marker, 
                            horizontalalignment='center', verticalalignment='center', 
                            fontsize=20, fontname='Segoe UI Emoji', color='blue', zorder=3)
                except:
                    ax.text(pos[0], pos[1], "R", 
                            horizontalalignment='center', verticalalignment='center', 
                            fontsize=14, fontweight='bold', color='blue', zorder=3)
            plt.draw()

        # --- Button Logic ---
        def next_step(event):
            if state['index'] < len(history) - 1:
                state['index'] += 1
                draw_frame(state['index'])
            elif state['playing']: 
                # If playing and reached the end, stop automatically
                toggle_play(None)

        def prev_step(event):
            if state['index'] > 0:
                state['index'] -= 1
                draw_frame(state['index'])

        # --- Timer Logic for Auto-Play ---
        # Interval=800 means 0.8 seconds per step.
        timer = fig.canvas.new_timer(interval=800) 
        timer.add_callback(next_step, None)

        def toggle_play(event):
            if state['playing']:
                # STOP
                timer.stop()
                state['playing'] = False
                bplay.label.set_text("Play")
            else:
                # START
                # If we are already at the end, restart from 0
                if state['index'] >= len(history) - 1:
                    state['index'] = 0
                    draw_frame(0)
                
                timer.start()
                state['playing'] = True
                bplay.label.set_text("Pause")
        
        # --- NEW: Save GIF Logic ---
        def save_gif(event):
            # 1. Stop playback if running so it doesn't conflict
            if state['playing']:
                toggle_play(None)
            
            # 2. Update button text to indicate processing
            print("Generating GIF... Please wait.")
            bsave.label.set_text("Saving...")
            plt.draw()
            fig.canvas.flush_events() 

            # 3. Create a writer
            writer = PillowWriter(fps=2)
            outfile = "robot_simulation.gif"

            # 4. Save loop
            with writer.saving(fig, outfile, dpi=100):
                for i in range(len(history)):
                    draw_frame(i)
                    writer.grab_frame()
            
            # 5. Restore UI
            print(f"Done! Saved as {outfile}")
            bsave.label.set_text("Save GIF")
            draw_frame(state['index']) # Restore view to where user was

        # --- Keyboard Support ---
        def on_key(event):
            if event.key == 'right': next_step(None)
            elif event.key == 'left': prev_step(None)
            elif event.key == ' ' or event.key == 'enter': toggle_play(None)

        # --- Create Buttons [left, bottom, width, height] ---
        # Adjusted positions to fit 4 buttons
        axprev = plt.axes([0.1, 0.05, 0.15, 0.075])
        axplay = plt.axes([0.3, 0.05, 0.15, 0.075])
        axnext = plt.axes([0.5, 0.05, 0.15, 0.075])
        axsave = plt.axes([0.7, 0.05, 0.20, 0.075]) # New Axis
        
        bprev = Button(axprev, 'Previous')
        bplay = Button(axplay, 'Play')
        bnext = Button(axnext, 'Next')
        bsave = Button(axsave, 'Save GIF') # New Button
        
        bprev.on_clicked(prev_step)
        bplay.on_clicked(toggle_play)
        bnext.on_clicked(next_step)
        bsave.on_clicked(save_gif) # New Callback
        
        fig.canvas.mpl_connect('key_press_event', on_key)

        # Initial Draw
        draw_frame(0)
        plt.show()


    # def visualize_robots(self, history, x_min, x_max, y_min, y_max):
    #     import matplotlib.pyplot as plt
    #     from matplotlib.widgets import Button
    #     import numpy as np
        
    #     # --- Setup the Figure ---
    #     # Make the figure slightly taller to fit buttons at the bottom
    #     fig, ax = plt.subplots(figsize=(8, 9)) 
    #     plt.subplots_adjust(bottom=0.2) # Create empty space at the bottom for buttons

    #     # Using a list to store the index allows us to modify it inside the button functions
    #     state = {'index': 0} 

    #     def draw_frame(i):
    #         """Helper function to clear and redraw the specific frame 'i'"""
    #         ax.clear()
            
    #         # --- Grid Settings ---
    #         ax.set_title(f"Iteration: {i} / {len(history)-1}")
    #         ax.set_xlim(x_min - 1, x_max + 1)
    #         ax.set_ylim(y_min - 1, y_max + 1)
    #         ax.set_aspect('equal')
            
    #         # Draw Grid Lines
    #         y_ticks = np.arange(int(y_min), int(y_max) + 2, 1)
    #         x_ticks = np.arange(int(x_min), int(x_max) + 2, 1)
    #         ax.set_yticks(y_ticks)
    #         ax.set_xticks(x_ticks)
    #         ax.grid(True, which='both', linestyle='--', linewidth=1, color='gray', alpha=0.5)

    #         # --- Draw Robots ---
    #         positions = history[i]
    #         robot_marker = "🤖" # You can change this to "●" or "R" if needed
            
    #         for pos in positions:
    #             # Try drawing the emoji, fallback to text if it fails
    #             try:
    #                 ax.text(pos[0], pos[1], robot_marker, 
    #                         horizontalalignment='center', verticalalignment='center', 
    #                         fontsize=20, fontname='Segoe UI Emoji', color='blue', zorder=3)
    #             except:
    #                 ax.text(pos[0], pos[1], "R", 
    #                         horizontalalignment='center', verticalalignment='center', 
    #                         fontsize=14, fontweight='bold', color='blue', zorder=3)

    #         plt.draw()

    #     # --- Button Callback Functions ---
    #     def next_step(event):
    #         if state['index'] < len(history) - 1:
    #             state['index'] += 1
    #             draw_frame(state['index'])

    #     def prev_step(event):
    #         if state['index'] > 0:
    #             state['index'] -= 1
    #             draw_frame(state['index'])
        
    #     # --- Keyboard Callback Function ---
    #     def on_key(event):
    #         if event.key == 'right':
    #             next_step(None)
    #         elif event.key == 'left':
    #             prev_step(None)

    #     # --- Create Buttons (Position: [left, bottom, width, height]) ---
    #     axprev = plt.axes([0.3, 0.05, 0.15, 0.075])
    #     axnext = plt.axes([0.55, 0.05, 0.15, 0.075])
        
    #     bprev = Button(axprev, 'Previous')
    #     bnext = Button(axnext, 'Next')
        
    #     # Connect actions
    #     bprev.on_clicked(prev_step)
    #     bnext.on_clicked(next_step)
    #     fig.canvas.mpl_connect('key_press_event', on_key) # Connect keyboard

    #     # Draw the first frame and show
    #     draw_frame(0)
    #     plt.show()

    # def visualize_robots(self, history, x_min, x_max, y_min, y_max):
    #     """
    #     Creates an animation of the robots moving based on the history list.
    #     """
    #     fig, ax = plt.subplots(figsize=(8, 8))
    #     ax.set_xlim(x_min - 1, x_max + 1)
    #     ax.set_ylim(y_min - 1, y_max + 1)
    #     ax.set_aspect('equal')
    #     # --- 2. Force Grid Lines at Every Integer (1, 2, 3, 4...) ---
    #     # This creates a list [0, 1, 2, 3, ... max_y]
    #     y_ticks = np.arange(int(y_min), int(y_max), 1)
    #     x_ticks = np.arange(int(x_min), int(x_max), 1)
        
    #     ax.set_yticks(y_ticks)
    #     ax.set_xticks(x_ticks)
    #     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    #     ax.set_title("Robot Movement Simulation")
    #     # Initialize the scatter plot with the first frame
    #     # We use separate lists for X and Y coordinates
    #     # initial_x = [pos[0] for pos in history[0]]
    #     # initial_y = [pos[1] for pos in history[0]]
    #     scat = ax.scatter([], [], c='blue', s=100, label='Robots')
    #     # scat = ax.scatter(initial_x, initial_y, c='blue', s=100, label='Robots')
    #     # Loop through every frame in history
    #     for i, positions in enumerate(history):
    #         # --- PASTE THE NEW CODE HERE (INSIDE THE LOOP) ---
    #         ax.clear()  # 1. Clear the previous frame
    #         # 2. Re-draw Grid & Settings (Must happen after clear)
    #         ax.set_title(f"Iteration: {i}")
    #         ax.set_xlim(x_min - 1, x_max + 1)
    #         ax.set_ylim(y_min - 1, y_max + 1)

    #         # Draw lines at every integer
    #         y_ticks = np.arange(int(y_min), int(y_max), 1)
    #         x_ticks = np.arange(int(x_min), int(x_max), 1)
    #         ax.set_yticks(y_ticks)
    #         ax.set_xticks(x_ticks)
    #         ax.grid(True, which='both', linestyle='--', linewidth=1, color='gray', alpha=0.5)

    #         # 3. Draw Emojis
    #         robot_emoji = "🤖" 
    #         for pos in positions:
    #             ax.text(pos[0], pos[1], robot_emoji, 
    #                     horizontalalignment='center', 
    #                     verticalalignment='center', 
    #                     fontsize=18,fontname='Segoe UI Emoji',color='blue', zorder=3)
    #         # Extract X and Y coordinates
    #         # xs = [p[0] for p in positions]
    #         # ys = [p[1] for p in positions]
            
    #         # # Update the dots
    #         # scat.set_offsets(list(zip(xs, ys)))
    #         # ax.set_title(f"Iteration: {i}")
            
    #         # Force matplotlib to draw this frame and wait
    #         plt.draw()
    #         plt.pause(1.0)  # Pause for 0.5 seconds (adjust this for speed)
        
    #     plt.ioff() # Turn off interactive mode
    #     plt.show() # Keep the final window open
    
    # ======================================= Different method to show the output =========================================
    # def display(self):
    #     console = Console()
    #     coords = {r.position(): r.name for r in self.robots}

    #     xs = [r.x for r in self.robots]
    #     ys = [r.y for r in self.robots]

    #     min_x, max_x = min(xs), max(xs)
    #     min_y, max_y = min(ys), max(ys)

    #     table = Table(show_header=False, box=None, padding=(0,1))

    #     j_counter = 1  # start j index from 1 at top

    #     # Build grid rows (top → bottom)
    #     for y in range(max_y, 0, -1):
    #         row = [str(y)]  # Y-axis on left
    #         for x in range(min_x, max_x+1):
    #           if y == 0:
    #             row.append(" ")  # leave empty in 0-row
    #           else:
    #             if (x,y) in coords:
    #                 row.append(Text("🤖", style="bold green"))
    #             else:
    #                 row.append(Text("✴", style="dim"))
    #         if (y!=0):row.append(str(j_counter))  # add j-axis on right
    #         j_counter += 1
    #         table.add_row(*row)

    #     # Add X-axis row at the bottom
    #     x_axis_row = ["Y/X"]  # left corner empty
    #     for x in range(min_x, max_x+1):
    #         x_axis_row.append(f"{x:2}")  # nicely formatted number
    #         # x_axis_row.append(str(x))
    #         # x_axis_row.extend(["", str(x)])
    #     x_axis_row.append("   J")  # mark right corner
    #     table.add_row(*x_axis_row)

    #     console.print(table)

    # def display(self):
    #     console = Console()
    #     coords = {r.position(): r.name for r in self.robots}

    #     xs = [r.x for r in self.robots]
    #     ys = [r.y for r in self.robots]

    #     table = Table(show_header=False, box=None, padding=(0,1))
        
    #     for y in range(max(ys), 0, -1):
    #         row = []
    #         for x in range(min(xs), max(xs)+1):
    #             if (x,y) in coords:
    #                 row.append(Text("🤖", style="bold green"))
    #             else:
    #                 row.append(Text("✴", style="dim"))
    #         table.add_row(*row)

    #     console.print(table)
#     =============================================================================================

# ---- Example Simulation ----
if __name__ == "__main__":

    # ================================= For distinct random 8 robots ===================================
    # robots = []
    # used_coords = set()

    # while len(robots) < 8:
    #     x = random.randint(0, 7)
    #     y = random.randint(1, 8)
    #     if (x, y) not in used_coords:
    #         used_coords.add((x, y))
    #         robots.append(Robot(x, y, f"r{len(robots) + 1}"))

    # scatter = GridScatter(robots)

    # ================================= For random 8 robots ===========================================
    # robots = [Robot(random.randint(0,5), random.randint(1,6), f"r{i+1}") for i in range(7)]
    # scatter = GridScatter(robots)
    # robots = [Robot(random.randint(0,10), random.randint(1,11), f"r{i+1}") for i in range(14)]
    # scatter = GridScatter(robots)

    # ================================ Manually place 8 robot's Sample ================================
    coords = [(1,1), (0,3), (1,5), (2,4), (2,3), (3,4), (5,6), (5,4)] # Base or main data
    # coords = [(1,2), (4,2), (2,3), (5,1), (3,2), (1,3), (4,3)]
    # coords = [(4,3), (7,3), (0,1), (2,5), (4,5), (2,3), (0,5), (0,3)]
    # coords = [(0,2), (3,2), (0,1), (4,4), (5,5), (1,2), (1,4), (0,3)]
    # coords = [(1,3), (0,5), (1,5), (0,1), (1,2), (5,2), (4,6), (4,1)]
    # coords = [(1,3), (5,1), (3,1), (5,6), (4,1), (1,4), (0,4), (1,6)]
    # coords = [(1,1), (0,3), (1,5), (0,4), (2,3), (2,4), (0,6), (4,4)]
    # [r1@(1,2), r2@(4,2), r3@(2,3), r4@(5,1), r5@(3,2), r6@(1,3), r7@(4,3)] # Not working but random
    # [r1@(5,1), r2@(2,6), r3@(5,3), r4@(5,1), r5@(5,4), r6@(1,4), r7@(0,3)] # Not working for 7 robots
    # coords = [(3,3), (1,6), (6,5), (8,7), (5,1), (0,2), (2,1), (5,8), (1,4), (4,7), (1,1), (4,3)]
    # coords = [(0,1), (2,9), (7,8), (3,2), (8,7), (8,3), (2,5), (5,8), (4,7), (4,2), (2,3), (0,2)]
    # coords = [(4,9), (5,5), (8,8), (1,8), (6,9), (1,9), (6,3), (2,8), (8,4), (8,6), (2,4), (2,3)] # Not working
    # coords = [(0,4), (3,0), (3,5), (1,5), (0,5), (4,1), (5,4), (1,5)] # goes to infinity loop
    # coords = [(0,4), (3,2), (3,5), (1,5), (0,5), (4,1), (5,4), (5,5)] # working
    # coords = [(1,2), (0,4), (1,6), (2,4), (4,4), (3,4), (5,6), (5,4)] # after case 1 and 2
    # coords = [(0,2), (0,4), (0,6), (2,4), (6,4), (4,4), (2,6), (8,4)] # after case 1 and 2 and 3
    
    # coords = [(5,4), (4,2), (3,7), (6,7), (6,4), (2,2), (3,1), (5,6)]
    # coords = [(8,4), (2,1), (8,5), (6,2), (2,8), (3,6), (8,7), (2,6), (3,2), (2,3)] # NOt Solved
    # coords = [(3,5), (1,4), (3,6), (2,5), (5,1), (0,2), (4,2)]
    robots = [Robot(x, y, f"r{i+1}") for i, (x,y) in enumerate(coords)]
    scatter = GridScatter(robots)
    # =====================================================================================
    # [r1@(3,5), r2@(1,4), r3@(3,6), r4@(2,5), r5@(5,1), r6@(0,2), r7@(4,2)] # 10.11.25
    # [r1@(5,5), r2@(1,7), r3@(3,4), r4@(1,6), r5@(5,7), r6@(0,6), r7@(2,5)] # Actual output of 7 robots
    # [r1@(8,4), r2@(2,1), r3@(8,5), r4@(6,2), r5@(2,8), r6@(3,6), r7@(8,7), r8@(2,6), r9@(3,2), r10@(2,3)] 10.11.25
    # [r1@(5,4), r2@(4,2), r3@(3,7), r4@(6,7), r5@(6,4), r6@(2,2), r7@(3,1), r8@(5,6)] # 9.11.25

    # [r1@(4,9), r2@(5,5), r3@(8,8), r4@(1,8), r5@(6,9), r6@(1,9), r7@(6,3), r8@(2,8), r9@(8,4), r10@(8,6), r11@(2,4), r12@(2,3)] # Not Working
    # [r1@(1,3), r2@(1,5), r3@(5,6), r4@(1,7), r5@(2,3), r6@(3,4), r7@(3,2), r8@(4,6), r9@(1,8), r10@(8,6), r11@(7,8), r12@(6,3)] # Not Working
    # [r1@(0,1), r2@(2,9), r3@(7,8), r4@(3,2), r5@(8,7), r6@(8,3), r7@(2,5), r8@(5,8), r9@(4,7), r10@(4,2), r11@(2,3), r12@(0,2)] # Working
    # [r1@(3,3), r2@(1,6), r3@(6,5), r4@(8,7), r5@(5,1), r6@(0,2), r7@(2,1), r8@(5,8), r9@(1,4), r10@(4,7), r11@(1,1), r12@(4,3)] # Working
    # [r1@(1,3), r2@(0,5), r3@(1,5), r4@(0,1), r5@(1,2), r6@(5,2), r7@(4,6), r8@(4,1)] # Working
    # [r1@(1,3), r2@(5,1), r3@(3,1), r4@(5,6), r5@(4,1), r6@(1,4), r7@(0,4), r8@(1,6)] # Working
    # [r1@(1,1), r2@(0,3), r3@(1,5), r4@(0,4), r5@(2,3), r6@(2,4), r7@(0,6), r8@(4,4)] # NOt required
    # r1@(4,3), r2@(7,3), r3@(0,1), r4@(2,5), r5@(4,5), r6@(2,3), r7@(0,5), r8@(0,3)
    # [r1@(0,2), r2@(0,4), r3@(0,6), r4@(2,4), r5@(6,4), r6@(4,4), r7@(2,6), r8@(8,4)]
    # [r1@(0,2), r2@(3,2), r3@(0,1), r4@(4,4), r5@(5,5), r6@(1,2), r7@(1,4), r8@(0,3)]
    # [r1@(0,4), r2@(3,0), r3@(3,5), r4@(1,5), r5@(0,5), r6@(4,1), r7@(5,4), r8@(1,5)]

    print(robots)
    print("Initial:")
    scatter.display()

    # number_of_iteration = scatter.form_grid()

    print("\nFinal:")
    print(robots)
    scatter.display()
    

    # # Calculate grid bounds for the plot
    all_xs = [r.x for r in robots] # Note: this uses final positions, usually safe for bounds
    all_ys = [r.y for r in robots]

    print("Calculating movement...")
    
    # Capture the history returned by the modified function
    iterations, history_data = scatter.form_grid() 
    # my_anim = scatter.visualize_robots(history_data, x_min=min(all_xs)-2, x_max=max(all_xs)+5, y_min=0, y_max=max(all_ys)+2)
    print(f"Simulation finished in {iterations} iterations.")
    print(f"No of Iteration for this case = {iterations}")
    # 2. Now call plt.show() to keep the window open
    # plt.show()
    print(f"Total Frames: {len(history_data)}")
    if len(history_data) <= 1:
        print("WARNING: Robots did not move! Check your logic conditions.")
    
    # # Start the visual animation
    # # Adjust range (e.g., 0 to 15) based on your specific grid size expectations
    scatter.visualize_robots(history_data, x_min=min(all_xs)-2, x_max=max(all_xs)+5, y_min=0, y_max=max(all_ys)+2)
