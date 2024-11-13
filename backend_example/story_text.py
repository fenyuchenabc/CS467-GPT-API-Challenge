from time import sleep 
from openai import OpenAI 
import os 
from dotenv import load_dotenv
from database import StoryDatabase

load_dotenv()

class Author:
    def __init__(self):
        """
        Represents an author that writes stories.
        """
        writer_job = """You are an author for childrens books. Your job is to create
                        choose your own adventure style stories giving the child
                        the option to select various paths in a story. Stories should vary
                        based on genre and age of the child"""
        self.db = None  # Initialize self.db
        
        try:
            self.client = OpenAI(api_key=os.getenv("GPT_API_KEY")) #whatever our key is
            self.assistant = self.client.beta.assistants.create(
                    name="Script Writer",
                    instructions= writer_job,
                    model = 'gpt-4o-mini-2024-07-18' #whatever model we end up using
                )
            self.thread = self.create_thread()
        except Exception as e:
            print(f"Error initializing Author: {e}")

        # Ensure self.db is always initialized
        try:
            self.db = StoryDatabase()
        except Exception as e:
            print(f"Error initializing StoryDatabase: {e}")

    def create_thread(self):
        try:
            thread = self.client.beta.threads.create()
            return thread
        except Exception as e:
            print(f"Error creating thread: {e}")
            return None
    
    def create_message(self, text_input):
        """
        Creates a message for GPT to read. Similar to a text input on the web app.
        """
        try:
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=text_input,
            )
            return message
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
        
    def writer_thread(self):
        return self.thread

    def execute(self, text_input):
        """
        Executes the input given by the user.
        """
        try:
            message = self.create_message(text_input=text_input)
            run = self.client.beta.threads.runs.create(
                thread_id = self.thread.id,
                assistant_id = self.assistant.id,
            )
            while run.status == 'queued' or run.status == 'in_progress':
                run = self.client.beta.threads.runs.retrieve(
                    thread_id = self.thread.id,
                    run_id=run.id,
                )
                sleep(.5)
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id,
                order='asc',
                after=message.id
                )
            for m in messages:
                response_text = m.content[0].text.value
                if "The End" in response_text or "end of the story" in response_text:
                    print(response_text)
                    print("")
                    self.db_close()
                    return "Thank you for reading. The story has concluded!"
                return response_text
        except Exception as e:
            print(f"Error executing story generation: {e}")
            return "Error during story generation"
    
    def first_page(self, genre, age, choice_count, length, key_moments=None):
        """
        Initializes the story based on the provided parameters by the reader.
        """
        command = f"""Write the first page of an interactive {genre} story for a {age} year
                    old child. Give the reader {choice_count} choices per story segment. Only create one
                    segment at a time before hearing what the reader chooses then move on from there. Try to keep
                    the story to a {length} length. Always end the story with "The End" and
                    don't say anything past that. No need to give "turn to page" sections at the end of choices."""
        if key_moments:
            command += f" During the story, incorporate the following key moments given by the reader: {key_moments}"
        response = self.execute(command)
        if response and response != "Error during story generation":
            try:
                self.db.save_story(genre, age, choice_count, length, response)
            except Exception as e:
                print(f"Error saving story to database: {e}")
        return response

    def db_close(self):
        self.db.close()

def main():
    agent = Author()
    print('Ready!')
    try:
        # Convert inputs to integers with error handling
        try:
            age = int(input("How old are you?: "))
            page_count = input("How long should this story be? (Short, Medium, Long): ")
            choice_count = int(input("How many options would you like per section?: "))
            key_moments = input(
            "Are there any particular events you want to happen in this story? (Optional. Press Enter to skip.): ")
        except ValueError:
            print("Invalid input. Please enter numeric values for age, page count, and choice count.")
            return  # Exit the function if input is invalid

        genre = input("What genre of story would you like to hear?: ")

        # Generate the first page of the story
        response = agent.first_page(genre, age, choice_count, page_count, key_moments)
        print(response)
        
        # Interactive loop for continuing the story
        while True:
            text = input("Adventurer: ")
            if text.upper() == 'EXIT':
                print('Goodbye!')
                sleep(2)
                break
                
            response = agent.execute(text)
            print("")
            if "The story has concluded" in response:
                print(response)
                print("")
                break
            print('Author: ', response)
            print()
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        agent.db_close()

if __name__ == '__main__':
    main()
    