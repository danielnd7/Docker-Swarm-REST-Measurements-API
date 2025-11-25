This is the best way to learn. I will guide you through the logic and structure so you can write the code yourself.

[cite_start]Since you decided to use **RedisTimeSeries** (which is the correct choice for the assignment [cite: 10]), the commands will differ slightly from a standard Redis List.

Here is your step-by-step guide to writing `main.py`.

### Step 1: Imports
You need to import the necessary tools.
* **`os`**: To read environment variables (crucial for Docker later).
* [cite_start]**`socket`**: To get the container ID/Hostname[cite: 18].
* **`time`**: Useful if you want to generate manual timestamps (though Redis can do it for you).
* **`flask`**: Import `Flask` and `request`.
* **`redis`**: The database client.

### Step 2: Configuration & Connection
This is where you prepare the app to survive inside a container.
* **Define the Host:** Do **not** hardcode `'localhost'`. Use `os.getenv('REDIS_HOST', 'localhost')`. [cite_start]This tells Python: *"Try to find a variable named REDIS_HOST; if it doesn't exist, default to localhost."*[cite: 43].
* **Define the Port:** Standard Redis port is `6379`.
* **Connect:** Create your Redis client object (e.g., `r = ...`).
    * *Hint:* Pass `decode_responses=True` so you get text back instead of bytes.

### Step 3: The "Setup" Block (Optional but Recommended)
RedisTimeSeries requires a key to exist before you add data (or you can create it on the fly).
* Write a small `try-except` block that runs when the app starts.
* Try to create a TimeSeries key (e.g., `mediciones`) using a command like `r.ts().create('mediciones')`.
* *Hint:* Handle the exception `ResponseError` in case the key already exists (so your app doesn't crash on restart).

### Step 4: The `/nuevo` Endpoint
[cite_start]This is for **input**[cite: 13].
1.  **Define the route:** `@app.route(...)`.
2.  [cite_start]**Get the data:** Use `request.args.get('dato')` to grab the value from the URL[cite: 34].
3.  **Validate:** Ensure the data is not empty and is a valid number (float).
4.  **Save to Redis (The TimeSeries way):**
    * Instead of `rpush`, look for the **TimeSeries** add command.
    * *Syntax Hint:* `r.ts().add(key, timestamp, value)`
    * *Pro Tip:* If you pass `'*'` as the timestamp, Redis automatically uses the current server time.
5.  **Return:** A confirmation message (e.g., "Saved").

### Step 5: The `/Listar` Endpoint
[cite_start]This is for **output**[cite: 16].
1.  **Define the route.**
2.  **Get the Hostname:** Use `socket.gethostname()`. [cite_start]This is required to prove which container answered the request later in the Swarm[cite: 18].
3.  **Retrieve Data:**
    * You need the **Range** command for TimeSeries.
    * *Syntax Hint:* `r.ts().range('mediciones', from_time, to_time)`
    * *Pro Tip:* Use `'-'` for the start time (beginning of time) and `'+'` for the end time (now) to get everything.
4.  **Format the Output:**
    * The `range` command returns a list of tuples: `[(timestamp1, value1), (timestamp2, value2)]`.
    * You need to loop through this list and format it into a string (e.g., using HTML `<br>` tags for line breaks).
5.  **Return:** A string containing the Hostname and the formatted list of values.

### Step 6: The Execution Block
Standard Python boilerplate.
* `if __name__ == "__main__":`
* `app.run(...)`
* *Hint:* Set `host='0.0.0.0'` so the server is accessible externally (required for Docker containers).

---

### 💡 Quick Check: How to test `ts().add`?
If you are stuck on the syntax for Step 4, you can test it in your terminal before coding:
1.  Go to **http://localhost:8001** (RedisInsight).
2.  Open the "Workbench" or "CLI".
3.  Type: `TS.ADD mediciones * 25.5`
4.  If that works, the Python equivalent is `r.ts().add('mediciones', '*', 25.5)`.

Give it a try! If you get stuck on a specific error, paste it here and I will help you debug.