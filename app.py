import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🏠 ਲੈਂਡਿੰਗ ਪੇਜ (ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਦੇਖਣ ਲਈ)
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="pa">
    <head>
        <meta charset="UTF-8">
        <title>Saini Bots - DRM API</title>
        <style>
            body { background-color: #121212; color: #ff0000; font-family: monospace; text-align: center; padding-top: 50px; }
            .container { border: 2px solid #ff0000; display: inline-block; padding: 20px; border-radius: 10px; }
            pre { font-size: 12px; line-height: 1.2; }
            h2 { color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <pre>
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░█░▄▄▀█▄░▄██░▀██░█▄░▄██
██▄▄▄▀▀█░▀▀░██░███░█░█░██░███
██░▀▀▀░█░██░█▀░▀██░██▄░█▀░▀██
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
            </pre>
            <h2>Powered By SAINI BOTS</h2>
            <p style="color: #888;">DRM Key Extractor API is Running...</p>
        </div>
    </body>
    </html>
    """

# 🔑 ਮੇਨ API ਐਂਡਪੁਆਇੰਟ
@app.route('/extract_keys', methods=['GET'])
def extract_keys():
    # ਟੈਲੀਗ੍ਰਾਮ ਬੋਟ ਤੋਂ ਆਇਆ ਲਿੰਕ
    mpd_url = request.args.get('url')
    
    if not mpd_url:
        return jsonify({"status": "failed", "message": "ਕਿਰਪਾ ਕਰਕੇ URL ਪ੍ਰਦਾਨ ਕਰੋ"}), 400

    try:
        # ਇੱਥੇ T00LK1D ਦੀ main.py ਨੂੰ ਕਮਾਂਡ ਦਿੱਤੀ ਜਾਵੇਗੀ
        # ਨੋਟ: ਯਕੀਨੀ ਬਣਾਓ ਕਿ main.py ਤੁਹਾਡੇ ਫੋਲਡਰ ਵਿੱਚ ਮੌਜੂਦ ਹੈ
        process = subprocess.Popen(
            ['python3', 'main.py', mpd_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return jsonify({
                "status": "success",
                "extracted_keys": stdout.strip(),
                "provider": "SAINI BOTS"
            })
        else:
            return jsonify({"status": "error", "details": stderr}), 500

    except Exception as e:
        return jsonify({"status": "exception", "error": str(e)}), 500

if __name__ == "__main__":
    # Render ਲਈ ਪੋਰਟ ਸੈਟਿੰਗ
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
