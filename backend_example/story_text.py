from time import sleep 
from openai import OpenAI 
import os 
from dotenv import load_dotenv
from database import StoryDatabase

load_dotenv()

class Author:
    def __init__(self):
        writer_job = """You are an author for childrens books. Your job is to create
                        choose your own adventure style stories giving the child
                        the option to select various paths in a story. Stories should vary
                        based on genre and age of the child"""
        
        self.client = OpenAI(api_key=os.getenv("GPT_API_KEY")) #whatever our key is
        self.assistant = self.client.beta.assistants.create(
                name="Script Writer",
                instructions= writer_job,
                model = 'gpt-4o-mini-2024-07-18' #whatever model we end up using
            )
        self.thread = self.create_thread()

        self.db = StoryDatabase()

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread
    
    def create_message(self, text_input):
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=text_input,
        )
        return message
    
    def writer_thread(self):
        return self.thread

    def execute(self, text_input):
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
            return m.content[0].text.value
    
    def first_page(self, genre, age, choice_count, segment_count):
        command = f"""Write the first page of an interactive {genre} story for a {age} year
                    old child. Give the reader {choice_count} choices per story segment. Only create one
                    segment at a time before hearing what the reader chooses then move on from there. Keep the 
                    story to {segment_count} story segments overall before ending the story.
                    No need to give "turn to page" sections at the end of choices."""
        response = self.execute(command)

        self.db.save_story(genre, age, choice_count, segment_count, response)
        return response

    def db_close(self):
        self.db.close()

def main():
    agent = Author()
    print('Ready!')
    age = input("How old are you?: ")
    genre = input("What genre of story would you like to hear?: ")
    page_count = input("How many pages should this story be?: ")
    choice_count = input("How many options would you like per page?: ")
    response = agent.first_page(genre, age, choice_count, page_count)
    print(response)
    while True:
        text = input("USER: ")
        if text == 'EXIT':
            print('Goodbye!')
            sleep(2)
            Author.db_close()
            break 
        response = agent.execute(text)
        print('Author: ', response)
        print()

if __name__ == '__main__':
    main()