from eve import Eve
app = Eve()

if __name__ == '__main__':
    app.run(port=5002) # was conflicting with something on 5000