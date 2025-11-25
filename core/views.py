from django.shortcuts import render, redirect
from .models import Regi, Images
from cryptography.fernet import Fernet
import hashlib

def home(request):
    images = Images.objects.all()  # lowercase 'images' for context
    return render(request, 'home.html', {'images': images})  # key 'images'



def signup(request):
    if request.method == 'POST':
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted = cipher.encrypt(password.encode())

        obj = Regi(name=name, email=email, password=encrypted.decode(), key=key.decode())
        obj.save()

        return redirect('/login')

    return render(request, 'signup.html')


def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Regi.objects.get(email=email)
            cipher = Fernet(user.key.encode())
            decrypted_password = cipher.decrypt(user.password.encode()).decode()

            if password == decrypted_password:
                return redirect('home')  # success — redirect to home
            else:
                error = "Incorrect password."

        except Regi.DoesNotExist:
            error = "User does not exist."

        # if error happened, re-render login page with error message
        return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')


known_bad_hashes = [
    "d41d8cd98f00b204e9800998ecf8427e",  # Empty file hash
    "e99a18c428cb38d5f260853678922e03",  # Example dummy malicious file hash
]


def md5(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        file_hash = md5(uploaded_file)

        if file_hash in known_bad_hashes:
            result = f"⚠️ Keylogger signature detected! (Hash: {file_hash})"
        else:
            result = f"✅ File is clean. (Hash: {file_hash})"

        return render(request, 'result.html', {'result': result})

    return render(request, 'upload.html')



def awareness(request):
    return render(request,'awareness.html')