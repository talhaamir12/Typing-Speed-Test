#Author: Talha Amir
# Import all the required libraries
import pygame
from pygame.locals import *
import sys
import time
import random
  
class TypingGame:
   
    def __init__(self):
        self.w = 750 # the width of the window
        self.h = 500 # The height of the window
        self.reset = True 
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0

        #Results of the typing test
        self.accuracy = '0%'
        self.results = 'Time: 0 Accuracy: 0 % Wpm: 0 '
        self.wpm = 0

        self.end = False

        # RGB vlaues of the heading text, the sentence text and the text for the results
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (231, 202, 84)
        
        # pygame.init() initializes all imported pygame modules is a convenient way to get everything started
        pygame.init()

        # Loading the loading screen image
        self.open_img = pygame.image.load('Typing Speed Test (2).png')
        # Scaling the image to the width and height of the application
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))

        # Loading the background image 
        self.background = pygame.image.load('bg.png')
        self.background = pygame.transform.scale(self.background, (750,500))
        
        # Display the screen with the appropriate height and width
        self.screen = pygame.display.set_mode((self.w, self.h))
        # Caption is what the window is called at the top
        pygame.display.set_caption('Typing Speed test')

    '''   
    A function that will draw the text on the screen.
    The arguments it takes is the screen, the y coordinate of the screen to position our text,
    the message we want to draw,  
    the size of the font and color of the font.
    '''     
    def draw_text(self, screen, msg, y , fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center = (self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()   
    
    def get_sentence(self):
        sentence_file = open('sentences.txt').read() # Reading the sentences from the sentences.txt file
        sentences = sentence_file.split('\n') # Splitting the sentences by each line 
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if(not self.end):
            #Calculate time
            self.total_time = time.time() - self.time_start
               
            #Calculate the accuracy
            count = 0
            # Accuracy formula : (correct characters) x 100 / (total characters in sentence)
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1 # Incrementing count by 1 everytime a the user enters a correct letter
                except:
                    pass
            self.accuracy = count/len(self.word)*100 
           
            # Calculate words per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)
            
            # Displaying the results 
            self.results = 'Time:' + str(round(self.total_time)) +" secs   Accuracy:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))

            # draw icon image
            self.time_img = pygame.image.load('icon.png') # reset icon
            self.time_img = pygame.transform.scale(self.time_img, (150,150)) # Scaling the icon image
            screen.blit(self.time_img, (self.w/2-75,self.h-140))
            self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100)) # Drawing the reset button text

            # Prinitng the results    
            print(self.results)
            # updating the display
            pygame.display.update()

    # Main method
    def run(self):
        # resets all the variables
        self.reset_game()
    
       
        self.running=True
        # The loop will look for the mouse and keyboard events. 
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (50,250,650,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (50,250,650,50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x >= 50 and x <= 650 and y >= 250 and y <= 300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     # position of reset box
                    if(x >= 310 and x <= 510 and y >= 390 and self.end):
                        self.reset_game()
                        x,y = pygame.mouse.get_pos()
         
                        
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,350, 28, self.RESULT_C)  
                            self.end = True
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            
            pygame.display.update()
             
                
        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(1)
        
        self.reset = False
        self.end = False

        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence 
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()
        # Drawing heading
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80,self.HEAD_C)  
        # Draw the rectangle for input box
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)

        # Draw the sentence string
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)
        
        pygame.display.update()


TypingGame().run()