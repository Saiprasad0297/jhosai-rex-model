import glob, os, llm, datetime

workspace_dir = r"C:\Users\saipr\OneDrive\Dokumen\AI_Notes\AI_First"
log_file = os.path.join(workspace_dir, "development_log.txt")

# 1. Gather all context: read project code files (.py, .js, .txt, etc.) AND the dev log
context_data = []
file_patterns = ["*.txt", "*.py", "*.json", "*.html", "*.css", "*.js"]

for pattern in file_patterns:
    for file_path in glob.glob(os.path.join(workspace_dir, pattern)):
        # Skip the script itself so it doesn't read its own code
        if os.path.basename(file_path) == "chat_with_files.py":
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            filename = os.path.basename(file_path)
            context_data.append(f"--- FILE: {filename} ---\n{f.read()}\n")

context = "\n".join(context_data)

print("\n==================================================")
print(f"🚀 DEV WORKSPACE ACTIVE: {workspace_dir}")
print("==================================================")
query = input("\n💻 Describe your next app feature or bug fix: ")

# 2. Package everything for the Stealth Ox Alpha model
system_prompt = (
    "You are an expert lead software engineer assisting with application development.\n"
    "Analyze the provided code files and past development logs to understand the current state of the app.\n"
    "Provide clear code updates, explanations, and specify what the next step should be."
)

model = llm.get_model("ox")
response = model.prompt(
    f"Context from project files and past history:\n{context}\n\nUser Request: {query}",
    system=system_prompt
)
ai_response = response.text()

print("\n================== AI CODE & RESPONSE ==================\n")
print(ai_response)
print("\n========================================================")

# 3. Save this interaction cleanly to your permanent development log
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a", encoding="utf-8") as log:
    log.write(f"\n==================================================\n")
    log.write(f"📅 TIMESTAMP: {timestamp}\n")
    log.write(f"🧑‍💻 USER TARGET: {query}\n")
    log.write(f"\n🤖 AI DEVELOPMENT UPDATES:\n{ai_response}\n")
    log.write(f"==================================================\n")

print(f"\n💾 Progress saved to: development_log.txt")
