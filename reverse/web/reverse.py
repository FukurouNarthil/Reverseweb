def save_uploaded_file(f):
    with open('some/file/test.exe', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)