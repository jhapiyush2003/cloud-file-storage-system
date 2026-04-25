{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyN3MtYkvIVylx4RNsfeDr8+",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/jhapiyush2003/cloud-file-storage-system/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 383
        },
        "id": "Hb2tKC_0jxdf",
        "outputId": "dc4bc951-3a03-4d05-a8ae-f499f7e4d846"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_11373/2269278308.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[0;31m# Run: streamlit run app.py\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 5\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      6\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0msqlite3\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      7\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mos\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "# app.py\n",
        "# Mini Google Drive / Cloud File Storage System\n",
        "# Run: streamlit run app.py\n",
        "\n",
        "import streamlit as st\n",
        "import sqlite3\n",
        "import os\n",
        "import hashlib\n",
        "from datetime import datetime\n",
        "\n",
        "# -----------------------\n",
        "# CONFIG\n",
        "# -----------------------\n",
        "st.set_page_config(page_title=\"Mini Google Drive\", layout=\"wide\")\n",
        "\n",
        "UPLOAD_FOLDER = \"storage\"\n",
        "DB_NAME = \"cloud_storage.db\"\n",
        "\n",
        "if not os.path.exists(UPLOAD_FOLDER):\n",
        "    os.makedirs(UPLOAD_FOLDER)\n",
        "\n",
        "# -----------------------\n",
        "# DATABASE\n",
        "# -----------------------\n",
        "conn = sqlite3.connect(DB_NAME, check_same_thread=False)\n",
        "c = conn.cursor()\n",
        "\n",
        "c.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS users (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    username TEXT UNIQUE,\n",
        "    password TEXT\n",
        ")\n",
        "\"\"\")\n",
        "\n",
        "c.execute(\"\"\"\n",
        "CREATE TABLE IF NOT EXISTS files (\n",
        "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
        "    username TEXT,\n",
        "    filename TEXT,\n",
        "    filepath TEXT,\n",
        "    size INTEGER,\n",
        "    upload_time TEXT\n",
        ")\n",
        "\"\"\")\n",
        "conn.commit()\n",
        "\n",
        "# -----------------------\n",
        "# HELPERS\n",
        "# -----------------------\n",
        "def hash_password(password):\n",
        "    return hashlib.sha256(password.encode()).hexdigest()\n",
        "\n",
        "def signup(username, password):\n",
        "    try:\n",
        "        c.execute(\"INSERT INTO users (username,password) VALUES (?,?)\",\n",
        "                  (username, hash_password(password)))\n",
        "        conn.commit()\n",
        "        return True\n",
        "    except:\n",
        "        return False\n",
        "\n",
        "def login(username, password):\n",
        "    c.execute(\"SELECT * FROM users WHERE username=? AND password=?\",\n",
        "              (username, hash_password(password)))\n",
        "    return c.fetchone()\n",
        "\n",
        "def get_user_files(username):\n",
        "    c.execute(\"SELECT * FROM files WHERE username=?\", (username,))\n",
        "    return c.fetchall()\n",
        "\n",
        "def get_total_storage(username):\n",
        "    c.execute(\"SELECT SUM(size) FROM files WHERE username=?\", (username,))\n",
        "    data = c.fetchone()[0]\n",
        "    return data if data else 0\n",
        "\n",
        "# -----------------------\n",
        "# SESSION\n",
        "# -----------------------\n",
        "if \"logged_in\" not in st.session_state:\n",
        "    st.session_state.logged_in = False\n",
        "\n",
        "if \"username\" not in st.session_state:\n",
        "    st.session_state.username = \"\"\n",
        "\n",
        "# -----------------------\n",
        "# LOGIN PAGE\n",
        "# -----------------------\n",
        "if not st.session_state.logged_in:\n",
        "\n",
        "    st.title(\"☁️ Mini Google Drive\")\n",
        "    menu = st.sidebar.selectbox(\"Menu\", [\"Login\", \"Signup\"])\n",
        "\n",
        "    if menu == \"Signup\":\n",
        "        st.subheader(\"Create Account\")\n",
        "        new_user = st.text_input(\"Username\")\n",
        "        new_pass = st.text_input(\"Password\", type=\"password\")\n",
        "\n",
        "        if st.button(\"Signup\"):\n",
        "            if signup(new_user, new_pass):\n",
        "                st.success(\"Account created successfully!\")\n",
        "            else:\n",
        "                st.error(\"Username already exists.\")\n",
        "\n",
        "    if menu == \"Login\":\n",
        "        st.subheader(\"Login\")\n",
        "        user = st.text_input(\"Username\")\n",
        "        pw = st.text_input(\"Password\", type=\"password\")\n",
        "\n",
        "        if st.button(\"Login\"):\n",
        "            if login(user, pw):\n",
        "                st.session_state.logged_in = True\n",
        "                st.session_state.username = user\n",
        "                st.rerun()\n",
        "            else:\n",
        "                st.error(\"Invalid Login\")\n",
        "\n",
        "# -----------------------\n",
        "# DASHBOARD\n",
        "# -----------------------\n",
        "else:\n",
        "    username = st.session_state.username\n",
        "\n",
        "    st.sidebar.success(f\"Welcome {username}\")\n",
        "    page = st.sidebar.radio(\"Navigation\",\n",
        "                            [\"Upload File\", \"My Files\", \"Search Files\"])\n",
        "\n",
        "    if st.sidebar.button(\"Logout\"):\n",
        "        st.session_state.logged_in = False\n",
        "        st.rerun()\n",
        "\n",
        "    st.title(\"☁️ Cloud File Storage Dashboard\")\n",
        "\n",
        "    total = get_total_storage(username)\n",
        "    st.info(f\"Used Storage: {round(total/1024,2)} KB\")\n",
        "\n",
        "    # -----------------------\n",
        "    # UPLOAD\n",
        "    # -----------------------\n",
        "    if page == \"Upload File\":\n",
        "        st.subheader(\"Upload Files\")\n",
        "\n",
        "        file = st.file_uploader(\"Choose File\")\n",
        "\n",
        "        if file:\n",
        "            save_path = os.path.join(UPLOAD_FOLDER, file.name)\n",
        "\n",
        "            with open(save_path, \"wb\") as f:\n",
        "                f.write(file.getbuffer())\n",
        "\n",
        "            size = os.path.getsize(save_path)\n",
        "\n",
        "            c.execute(\"\"\"\n",
        "            INSERT INTO files(username,filename,filepath,size,upload_time)\n",
        "            VALUES (?,?,?,?,?)\n",
        "            \"\"\", (\n",
        "                username,\n",
        "                file.name,\n",
        "                save_path,\n",
        "                size,\n",
        "                datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")\n",
        "            ))\n",
        "            conn.commit()\n",
        "\n",
        "            st.success(\"File Uploaded Successfully!\")\n",
        "\n",
        "    # -----------------------\n",
        "    # MY FILES\n",
        "    # -----------------------\n",
        "    elif page == \"My Files\":\n",
        "        st.subheader(\"My Uploaded Files\")\n",
        "\n",
        "        files = get_user_files(username)\n",
        "\n",
        "        for f in files:\n",
        "            file_id = f[0]\n",
        "            filename = f[2]\n",
        "            path = f[3]\n",
        "            size = round(f[4]/1024, 2)\n",
        "            time = f[5]\n",
        "\n",
        "            col1, col2, col3 = st.columns([4,2,2])\n",
        "\n",
        "            with col1:\n",
        "                st.write(f\"📄 {filename} ({size} KB)\")\n",
        "                st.caption(time)\n",
        "\n",
        "            with col2:\n",
        "                with open(path, \"rb\") as file_data:\n",
        "                    st.download_button(\n",
        "                        \"Download\",\n",
        "                        file_data,\n",
        "                        file_name=filename,\n",
        "                        key=f\"down{file_id}\"\n",
        "                    )\n",
        "\n",
        "            with col3:\n",
        "                if st.button(\"Delete\", key=f\"del{file_id}\"):\n",
        "                    os.remove(path)\n",
        "                    c.execute(\"DELETE FROM files WHERE id=?\", (file_id,))\n",
        "                    conn.commit()\n",
        "                    st.rerun()\n",
        "\n",
        "    # -----------------------\n",
        "    # SEARCH\n",
        "    # -----------------------\n",
        "    elif page == \"Search Files\":\n",
        "        st.subheader(\"Search Files\")\n",
        "\n",
        "        query = st.text_input(\"Enter filename\")\n",
        "\n",
        "        if query:\n",
        "            c.execute(\"\"\"\n",
        "            SELECT * FROM files\n",
        "            WHERE username=? AND filename LIKE ?\n",
        "            \"\"\", (username, f\"%{query}%\"))\n",
        "\n",
        "            results = c.fetchall()\n",
        "\n",
        "            for f in results:\n",
        "                st.write(\"📄\", f[2], \"-\", f[5])"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install streamlit -q"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "m-ijwvBbkIeB",
        "outputId": "c4af9303-cf5b-458e-fb5a-cdc0d614745c"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m9.1/9.1 MB\u001b[0m \u001b[31m60.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m11.3/11.3 MB\u001b[0m \u001b[31m89.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app.py & npx localtunnel --port 8501"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "jSvBRlAEkPhf",
        "outputId": "cbe62b7d-3653-4dbb-ffb6-020fde872c79"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[1G\u001b[0K⠙Usage: streamlit run [OPTIONS] [TARGET] [ARGS]...\n",
            "Try 'streamlit run --help' for help.\n",
            "\n",
            "Error: Invalid value: File does not exist: app.py\n",
            "\u001b[1G\u001b[0K⠹\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K⠧\u001b[1G\u001b[0K⠇\u001b[1G\u001b[0K⠏\u001b[1G\u001b[0K\u001b[1G\u001b[0JNeed to install the following packages:\n",
            "localtunnel@2.0.2\n",
            "Ok to proceed? (y) \u001b[20G^C\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile app.py\n",
        "\n",
        "import streamlit as st\n",
        "\n",
        "st.title(\"Cloud File Storage System\")\n",
        "st.write(\"App Running Successfully 🚀\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Q-utXretkd3W",
        "outputId": "9c61b468-7286-41b6-fcd3-cf510565b5b3"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app.py & npx localtunnel --port 8501"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "SClalEJtk3Vo",
        "outputId": "5b4e6c60-969c-481f-f7b4-7b2f2037d0cb"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[1G\u001b[0K⠙\u001b[1G\u001b[0K⠹\n",
            "Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.\n",
            "\u001b[0m\n",
            "\u001b[1G\u001b[0K⠸\u001b[1G\u001b[0K⠼\u001b[1G\u001b[0K⠴\u001b[1G\u001b[0K⠦\u001b[1G\u001b[0K\u001b[1G\u001b[0JNeed to install the following packages:\n",
            "localtunnel@2.0.2\n",
            "Ok to proceed? (y) \u001b[20G\u001b[0m\n",
            "\u001b[34m\u001b[1m  You can now view your Streamlit app in your browser.\u001b[0m\n",
            "\u001b[0m\n",
            "\u001b[34m  Local URL: \u001b[0m\u001b[1mhttp://localhost:8501\u001b[0m\n",
            "\u001b[34m  Network URL: \u001b[0m\u001b[1mhttp://172.28.0.12:8501\u001b[0m\n",
            "\u001b[34m  External URL: \u001b[0m\u001b[1mhttp://35.239.207.198:8501\u001b[0m\n",
            "\u001b[0m\n"
          ]
        }
      ]
    }
  ]
}