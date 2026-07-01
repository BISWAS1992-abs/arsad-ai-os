"""
Arsad AI OS
Main Entry Point
Version: 1.0
"""

from app import app


def main():
    print("===================================")
    print("🚀 Arsad AI OS Starting...")
    print("===================================")

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
