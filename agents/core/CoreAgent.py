import asyncio
import logging
from datetime import datetime
from termcolor import colored
import ray
from utils.core_utils import (
    get_active_onboarded_users,
    get_pending_questions,
    update_question_next_response
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@ray.remote
class UserActor:
    async def process_user(self, user: dict):
        """Process a single user's questions"""
        print(colored(f"\n▶️ Starting process for user: {user.get('name', 'Unknown')}", 'cyan'))
        try:
            print(colored(f"  📥 Fetching questions for user {user.get('name', 'Unknown')}", 'yellow'))
            questions = await get_pending_questions(user["_id"])
            
            if not questions:
                print(colored(f"  ℹ️ No pending questions found for user {user.get('name', 'Unknown')}", 'blue'))
                return
            
            print(colored(f"  📝 Processing {len(questions)} questions", 'yellow'))
            for question in questions:
                print(colored(
                    f"\n  📋 Question Details:\n"
                    f"    Question: '{question['question_text']}'\n"
                    f"    Event-Type: '{question['event_type']}'\n"
                    f"    User-Id: '{user['_id']}'\n"
                    f"    User-Name: '{user.get('name', 'Unknown')}'",
                    'white'))
                
                await update_question_next_response(
                    question["_id"], 
                    question["search_interval"]
                )
            print(colored(f"✅ Completed process for user: {user.get('name', 'Unknown')}\n", 'green'))
        except Exception as e:
            print(colored(f"  ❌ Error processing user {user['_id']}: {str(e)}", 'red'))
            raise

class CoreAgent:
    async def process_all_users(self):
        """Main processing function that runs every hour"""
        try:
            print(colored("\n🚀 Starting user processing cycle...", 'magenta', attrs=['bold']))
            
            print(colored("🔍 Fetching active users...", 'yellow'))
            users = await get_active_onboarded_users()
            
            if not users:
                print(colored("ℹ️ No active users found", 'blue'))
                return
            
            print(colored(f"👥 Found {len(users)} active users", 'cyan'))
            actors = [UserActor.remote() for _ in users]
            tasks = [actor.process_user.remote(user) for actor, user in zip(actors, users)]
            
            ray.get(tasks)
            
            print(colored("✨ Completed processing cycle\n", 'green', attrs=['bold']))
            
        except Exception as e:
            print(colored(f"❌ Error in process_all_users: {str(e)}", 'red', attrs=['bold'])) 