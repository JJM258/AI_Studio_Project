# Importing Libraries

import tkinter # tkinter is used for the game window and canvas
import random # import random is for the random number generation to move the snake

# Creating the Game Window

rows = 35    
colunns = 35              
size = 25                 

width = size * rows       
height = size * colunns 

# Creating the Q-learning Agent (Process dicussed in the PDF report)

MOVEMENT = [(0,-1),(0,1),(-1,0),(1,0)] 

learning_rate = 0.1                   
discount_factor = 0.9                    
exploration_rate = 1.0                     
episodes = 40         

Q = {}                                     

def current_state(enemy_x, enemy_y, player_x, player_y): 
    direction_x = 0 if player_x == enemy_x else (1 if player_x > enemy_x else -1) 
    direction_y = 0 if player_y == enemy_y else (1 if player_y > enemy_y else -1)
    return (direction_x, direction_y) 

def choose_an_action(state, enemy_movement, exploration_rate): 
    if state not in Q: 
        Q[state] = [0.0, 0.0, 0.0, 0.0] 

    if random.random() < exploration_rate: 
        action = random.randint(0, 3) 
    else: 
        q = list(Q[state]) 
        action = q.index(max(q))

    return action 

def update_q_table(state, action, reward, next_state):                                       
    if state not in Q:                                                                
        Q[state] = [0.0, 0.0, 0.0, 0.0]                                                
    if next_state not in Q:                                                            
        Q[next_state] = [0.0, 0.0, 0.0, 0.0]                                            

    old = Q[state][action]                                                             
    future = max(Q[next_state])                                                         
    Q[state][action] = old + learning_rate * (reward + discount_factor * future - old)  

# Training the "Enemy Snake" (Process dicussed in the PDF report)

print("Training Now")                                                                                  

for episode in range(episodes):                                                                        
    enemy_x, enemy_y = random.randint(0, colunns-1) * size, random.randint(0, rows-1) * size           
    player_x, player_y = random.randint(0, colunns-1) * size, random.randint(0, rows-1) * size         
    enemy_movement = random.randint(0, 3)                                                              

    for step in range(100):                                                                            
        state = current_state(enemy_x, enemy_y, player_x, player_y)                                    
        action = choose_an_action(state, enemy_movement, exploration_rate)                            

        action_x, action_y = MOVEMENT[action]                                                          
        next_enemy_x, next_enemy_y = enemy_x + action_x * size, enemy_y + action_y * size             

        if next_enemy_x < 0 or next_enemy_x >= width or next_enemy_y < 0 or next_enemy_y >= height:    
            Q[state][action] = Q[state][action] + learning_rate * (-50 - Q[state][action])           
            break                                                                                   

        old_distance = abs(player_x - enemy_x) + abs(player_y - enemy_y)                               
        enemy_x, enemy_y = next_enemy_x, next_enemy_y                                               
        enemy_movement = action                                                                        
        new_distance = abs(player_x - enemy_x) + abs(player_y - enemy_y)                              

        if enemy_x == player_x and enemy_y == player_y:                                                
            reward = 500                                                                               
            next_state = current_state(enemy_x, enemy_y, player_x, player_y)                          
            update_q_table(state, action, reward, next_state)                                          
            break                                                                                     
        else:                                                                                         
            reward = 1 if new_distance < old_distance else -1                                          
            next_state = current_state(enemy_x, enemy_y, player_x, player_y)                           
            update_q_table(state, action, reward, next_state)                                      

    exploration_rate = max(0.01, exploration_rate * 0.999)                                             

print(f"Training Complete, {len(Q)} states learned.") # This print how many unique states were visited during the training

# Writing the "Snake Game Code" - Credit to YouTube channel name "Kenny Yip Coding"
# YouTube Channel Link - https://www.youtube.com/watch?v=FtqWCo1_I4g

class tile: 
    def __init__(self, x, y):
        self.x = x 
        self.y = y 

window = tkinter.Tk() 
window.title("Snake Game")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width = width, height = height) 
canvas.pack() 
window.update() 

window_width = window.winfo_width() 
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth() 
screen_height = window.winfo_screenheight() 

x = int((screen_width/2) - (window_width/2)) 
y = int((screen_height/2) - (window_height/2)) 

window.geometry(f"{window_width}x{window_height}+{x}+{y}") 

snake = tile(5*size, 5*size) 
food = tile(15*size, 15*size) 
body = [] 
velocityx = 0 
velocityy = 0 
game_over = False 
score = 0 
highest_score = 0 

enemy_snake = tile(10*size, 10*size) 
enemy_body = [] 
enemy_velocityx = 1 
enemy_velocityy = 0 
max_body_length = 5 

def reset(): 
    global velocityx, velocityy, game_over, snake, food, body, score 
    global enemy_snake, enemy_body, enemy_velocityx, enemy_velocityy 

    snake = tile(5*size, 5*size) 
    food = tile(15*size, 15*size) 
    body = [] 
    velocityx = 0 
    velocityy = 0 
    game_over = False 
    score = 0
        
    enemy_snake = tile(10*size, 10*size)
    enemy_body = [] 
    enemy_velocityx = 1 
    enemy_velocityy = 0

def direction_and_reset(event):
    global velocityx, velocityy, game_over

    if event.keysym == "space": 
        reset() 
        draw() 
        return 

    if (game_over):  
        return

    if (event.keysym == "Up" and velocityy != 1):
        velocityx = 0
        velocityy = -1 
    elif (event.keysym == "Down" and velocityy != -1): 
        velocityx = 0 
        velocityy = 1 
    elif (event.keysym == "Left" and velocityx != 1): 
        velocityx = -1 
        velocityy = 0 
    elif (event.keysym == "Right" and velocityx != -1): 
        velocityx = 1
        velocityy = 0 

def move_enemy(): 
    global enemy_body, enemy_snake, enemy_velocityx, enemy_velocityy

    next_x = enemy_snake.x + enemy_velocityx * size 
    next_y = enemy_snake.y + enemy_velocityy * size 
    if next_x < 0 or next_x >= width: 
        enemy_velocityx *= -1 
    if next_y < 0 or next_y >= height: 
        enemy_velocityy *= -1 

    if random.random() < 0.1: 
        choices = [(1,0),(-1,0),(0,1),(0,-1)] 
        choices = [(direction_x,direction_y) for direction_x,direction_y in choices if not (direction_x == -enemy_velocityx and direction_y == -enemy_velocityy)] 
        enemy_velocityx, enemy_velocityy = random.choice(choices) 

    if len(enemy_body) < max_body_length:
        enemy_body.append(tile(enemy_snake.x, enemy_snake.y)) 

    for i in range(len(enemy_body)-1, -1, -1): 
        t = enemy_body[i] 
        if i == 0: 
            t.x = enemy_snake.x 
            t.y = enemy_snake.y 
        else: 
            t.x = enemy_body[i-1].x 
            t.y = enemy_body[i-1].y 

    enemy_snake.x += enemy_velocityx * size 
    enemy_snake.y += enemy_velocityy * size 


def move(): 
    global snake, game_over, food, body, score 

    if (game_over):
        return 

    if (snake.x < 0 or snake.x >= width or snake.y < 0 or snake.y >= height): 
        game_over = True 
        return 
    
    for t in body:                                 
        if (snake.x == t.x and snake.y == t.y):  
            game_over = True                       
            return                               
        
    if snake.x == enemy_snake.x and snake.y == enemy_snake.y: 
        game_over = True                        
        return                                     
    
    for t in enemy_body:                      
        if (snake.x == t.x and snake.y == t.y): 
            game_over = True                 
            return                              

    if snake.x == food.x and snake.y == food.y: 
       body.append(tile(food.x, food.y))      
       food.x = random.randint(0, colunns - 1) * size   
       food.y = random.randint(0, rows - 1) * size  
       score += 1                                 
    
    for i in range(len(body)-1, -1, -1):         
        t = body[i]                               
        if (i == 0):                               
            t.x = snake.x                        
            t.y = snake.y                   
        else:                                      
            last_tile = body[i-1]                
            t.x = last_tile.x                  
            t.y = last_tile.y                  

    snake.x += velocityx * size              
    snake.y += velocityy * size                  

    move_enemy()                                 

def draw():
    global snake, score, food, body, game_over, highest_score
    move()

    canvas.delete("all")

    if (game_over):
        if score > highest_score:
            highest_score = score

        canvas.create_text(width/2, height/2, font="Arial 20", text=f"Game Over: {score}", fill="white")
        canvas.create_text(width/2, height/2 + 30, font="Arial 15", text=f"Best Score: {highest_score}", fill="yellow")
        canvas.create_text(width/2, height/2 + 60, font="Arial 15", text="Press Space Bar to Reset Game", fill="lime green")
        return

    canvas.create_rectangle(snake.x, snake.y, snake.x + size, snake.y + size, fill="blue")
    canvas.create_rectangle(food.x, food.y, food.x + size, food.y + size, fill="yellow")

    for t in body:
        canvas.create_rectangle(t.x, t.y, t.x + size, t.y + size, fill="blue")

    canvas.create_rectangle(enemy_snake.x, enemy_snake.y, enemy_snake.x + size, enemy_snake.y + size, fill="red")
    
    for t in enemy_body:
        canvas.create_rectangle(t.x, t.y, t.x + size, t.y + size, fill="red")

    canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")
    canvas.create_text(width - 80, 20, font="Arial 10", text=f"Best: {highest_score}", fill="white")

    window.after(100, draw)
    
draw()

window.bind("<KeyRelease>", direction_and_reset)

window.mainloop()