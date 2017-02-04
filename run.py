from blue import app

if __name__ == '__main__':
    #app.run(debug=True)
    # get port assigned by OS else set it to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port,debug=True)