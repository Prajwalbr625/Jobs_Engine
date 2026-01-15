from flask import Flask, render_template_string, abort, request
import sqlite3
from src.processors.formatter import ContentFormatter
from src.models import Job
from config.settings import DB_PATH

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Simple HTML Templates with "Media-First" aesthetic (Clean, readable)

# Valid Jinja2 setup without inheritance complexity for single-file script
# We will inject the content into the layout using Python before rendering

LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        :root {
            --primary: #2563eb;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --bg: #f9fafb;
            --card-bg: #ffffff;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text-main);
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        header {
            margin-bottom: 40px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 20px;
        }
        h1 { font-size: 2.25rem; font-weight: 800; color: #111827; margin: 0; }
        .subtitle { color: var(--text-muted); font-size: 1.1rem; }
        
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            padding: 24px;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-2px);
        }
        .card h2 { margin-top: 0; color: var(--primary); }
        .card-meta {
            display: flex;
            gap: 15px;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 15px;
        }
        .tag {
            background: #dbeafe;
            color: #1e40af;
            padding: 2px 10px;
            border-radius: 9999px;
            font-weight: 500;
            font-size: 0.8rem;
        }
        a.read-more {
            display: inline-block;
            margin-top: 10px;
            color: var(--primary);
            text-decoration: none;
            font-weight: 600;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            color: var(--text-muted);
            text-decoration: none;
        }
        
        /* Filter Styles */
        .filters {
            margin-bottom: 30px;
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .filters form { display: flex; gap: 10px; flex-wrap: wrap; }
        .filters input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 1rem;
        }
        .filters button, .filters a.btn {
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }
        .filters button { background: var(--primary); color: white; }
        .filters a.btn { background: #f3f4f6; color: #374151; }
        
        /* Post Content Styles */
        .post-content h2, .post-content h3 { color: #111827; margin-top: 1.5em; }
        .post-content p { margin-bottom: 1em; }
        .post-content a { color: var(--primary); text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <!-- CONTENT_PLACEHOLDER -->
    </div>
</body>
</html>
"""

INDEX_CONTENT = """
    <header>
        <h1>IT Jobs Alert Engine</h1>
        <p class="subtitle">Latest curated opportunities for Tech Professionals</p>
    </header>
    
    <div class="filters">
        <form action="/" method="get">
            <input type="text" name="location" placeholder="Filter by Location (e.g. Bangalore, Remote)" value="{{ location_filter }}">
            <button type="submit">Filter</button>
            {% if location_filter %}
                <a href="/" class="btn">Clear</a>
            {% endif %}
        </form>
        <div style="margin-top: 10px; display: flex; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 0.9rem; color: #6b7280; align-self: center;">Quick Filters:</span>
            <a href="/?location=Remote" class="btn" style="padding: 5px 10px; font-size: 0.85rem;">Remote</a>
            <a href="/?location=Bengaluru" class="btn" style="padding: 5px 10px; font-size: 0.85rem;">Bengaluru</a>
            <a href="/?location=Mumbai" class="btn" style="padding: 5px 10px; font-size: 0.85rem;">Mumbai</a>
            <a href="/?location=Delhi" class="btn" style="padding: 5px 10px; font-size: 0.85rem;">Delhi</a>
            <a href="/?location=Hyderabad" class="btn" style="padding: 5px 10px; font-size: 0.85rem;">Hyderabad</a>
            <a href="/?location=Pune" class="btn" style="padding: 5px 10px; font-size: 0.85rem;">Pune</a>
        </div>
    </div>
    
    {% if not posts %}
        <p style="text-align: center; color: #6b7280; margin-top: 40px;">No jobs found matching your criteria.</p>
    {% endif %}
    
    {% for post in posts %}
    <div class="card">
        <div class="card-meta">
            <span>{{ post.fetched_at[:10] }}</span>
            <span class="tag">{{ post.role_category }}</span>
            <span class="tag">{{ post.experience_level }}</span>
        </div>
        <h2><a href="/post/{{ post.job_hash }}" style="text-decoration: none; color: inherit;">{{ post.title }}</a></h2>
        <p><strong>{{ post.company }}</strong> &bull; {{ post.location }}</p>
        <a href="/post/{{ post.job_hash }}" class="read-more">Read Details &rarr;</a>
    </div>
    {% endfor %}
"""

POST_CONTENT = """
    <a href="/" class="back-link">&larr; Back to Listings</a>
    <div class="card">
        <h1>{{ content.title }}</h1>
        <div class="post-content">
            {{ content.content | safe }}
        </div>
    </div>
"""

@app.route('/')
def index():
    location_filter = request.args.get('location', '').strip()
    
    conn = get_db_connection()
    if location_filter:
        query = "SELECT * FROM jobs WHERE location LIKE ? ORDER BY fetched_at DESC"
        jobs = conn.execute(query, (f'%{location_filter}%',)).fetchall()
    else:
        jobs = conn.execute('SELECT * FROM jobs ORDER BY fetched_at DESC').fetchall()
    conn.close()
    
    # Inject content into layout
    template = LAYOUT.replace("<!-- CONTENT_PLACEHOLDER -->", INDEX_CONTENT)
    return render_template_string(template, title="Latest Jobs", posts=jobs, location_filter=location_filter)

@app.route('/post/<job_hash>')
def post(job_hash):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM jobs WHERE job_hash = ?', (job_hash,)).fetchone()
    conn.close()
    
    if row is None:
        abort(404)
        
    # Reconstruct Job object to use Formatter
    from src.models import Job
    job = Job(
        title=row['title'],
        company=row['company'],
        location=row['location'],
        experience_level=row['experience_level'],
        role_category=row['role_category'],
        apply_url=row['apply_url'],
        source_name=row['source_name'],
        fetched_at=row['fetched_at'], # Format might need adjustment if datetime is strict
        job_hash=row['job_hash']
    )
    
    # Generate Blog Content
    blog_data = ContentFormatter.format_blog(job)
    
    template = LAYOUT.replace("<!-- CONTENT_PLACEHOLDER -->", POST_CONTENT)
    return render_template_string(template, title=blog_data['title'], content=blog_data)

if __name__ == '__main__':
    print("Starting Local Blog Preview on http://localhost:5050")
    app.run(debug=True, port=5050)
