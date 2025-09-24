from django.shortcuts import render


from neo.forms import UserForm
#importing http to send the responses
from django.http import HttpResponse

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.files.base import ContentFile


# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#Importing Models
from .models import UserProfileInfo
from .models import FileTransferInfo
from .models import UploadToBucket
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from datetime import datetime
from google.cloud import storage
from django.core.files.storage import default_storage
from django.http import FileResponse


from django.core.files.storage import default_storage
# Create your views here.


@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('index'))


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'neo/login.html', {})



def index(request):
    return render(request,'neo/index.html')



def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()


            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'neo/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

#function for file upload
@login_required
def file_upload(request):
    if request.method == 'POST':
        # First get the receiver name and file
        sender_user = request.user

        receiver_email = request.POST.get('reciever_email')

        secret_key = request.POST.get('secret_key')
        
        upload_file = request.FILES['upload_file']

        fs = FileSystemStorage() #defaults to   MEDIA_ROOT  
        file_name = fs.save(upload_file.name, upload_file)

        file_url = fs.url(file_name)

        try:
            # Get the corresponding user with the provided email
            receiver_user = User.objects.get(email=receiver_email)
            
        except User.DoesNotExist:
            # Handle the case where the receiver user does not exist
            return HttpResponse("Receiver does not exist" )
        

        
        try:
            #Uploading file to GCP bucket

            import base64
            import os
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            password = secret_key

            password_res = bytes(password, 'utf-8')

            salt = 'lkjsadl;kfjhawlikercjnfowilcnehkrgjcinouw3ehfcn1kjqnwkefn90123848976592743(*&(*&^*%&^oiusjr0928374598237,ghdomilw3;eujf npqxoi34;luwrcjto js,rhgdkcmxlas'
            res = salt.encode('utf-8')
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt= res,
                iterations=480000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password_res))
            
            fernet = Fernet(key)
            from pathlib import Path
            import os
            # Build paths inside the project like this: BASE_DIR / 'subdir'.
            BASE_DIR = Path(__file__).resolve().parent.parent

            # to let django know where our media dir is
            MEDIA_DIR= os.path.join(BASE_DIR,"media")
            final_path = os.path.join(MEDIA_DIR,file_name)
 
            with open(final_path, 'rb') as file:
                original = file.read()

            encrypted = fernet.encrypt(original)

            with open(final_path, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)

            current_date = datetime.now()
            timestamp = current_date.strftime("%Y%m%d%H%M%S")
            object_path = f"{current_date.year}/{current_date.month}/{current_date.day}/{timestamp}_{upload_file}"
            
            with open(final_path,'r') as f:
                contents = f.read()
            
            byte_data = contents.encode('utf-8')

            # Create a ContentFile from byte data
            content_file = ContentFile(byte_data)
        
            object_uri = UploadToBucket.upload_files(content_file,object_path)
            # return HttpResponse("File Successfully Transferred")
            
        except Exception as e:
            print(e)
            return HttpResponse("Error while uploading file. Please try again after some time")
        
        FileTransferInfo.objects.create(sender=sender_user, sender_name=sender_user, receiver=receiver_user, file_path=object_path)

        success_data = {}
        success_data['file_name'] = upload_file
        success_data['receiver_email'] = receiver_email

        return render(request, 'neo/transfer_success.html', {'data':success_data})

    else:
        #rendering upload form
        return render(request, 'neo/upload.html', {})
    
#function for file dashboard
@login_required
def file_dashboard(request):
    current_user = request.user

    try:
        user_data_entries = FileTransferInfo.objects.filter(receiver=current_user).values()
        #user_data_entries = user_data_entries.filter(receiver=current_user)
        for data_entries in user_data_entries:
            data_entries['file_name'] = data_entries['file_path'].split('/')[-1]
            data_entries['file_name'] = data_entries['file_name'].split('+')[-1]

        return render(request,'neo/dashboard.html',{'user_data_entries': user_data_entries})
    except Exception as e:
        print(e)
        return HttpResponse("Error while loading file. Please try again after some time")

#function to download files
@login_required    
def show_file(request, file_path):
    file = {}
    file['file_path'] = file_path
    file['file_name'] = file_path.split('/')[-1]
    file['file_name'] = file['file_name'].split('+')[-1]
    #Render the download template with the file URL
    return render(request,'neo/download_file.html',{'file': file})

@login_required
def download_file(request):
    file_path = request.POST.get('file_path')
    file_path = f"files/{file_path}"
    file = default_storage.open(file_path)

    with default_storage.open(file_path, 'r') as gcs_file:
        # Get the content of the file
        file_content = gcs_file.read()
    
    file_name = request.POST.get('file_name')
    # print(type(file_name))


    from pathlib import Path
    import os
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # to let django know where our media dir is
    MEDIA_DIR= os.path.join(BASE_DIR,"media")
    final_path = os.path.join(MEDIA_DIR,file_name)

    print(final_path)

    file_result_data = file_content.decode('utf-8')

    with open(final_path, 'w') as django_file:
        # Write the content to the Django file
        django_file.write(file_result_data)
    
    import base64
    import os
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    key = request.POST.get('secret_key')

    try:
        password_dec = bytes(key, 'utf-8')

        salt = 'lkjsadl;kfjhawlikercjnfowilcnehkrgjcinouw3ehfcn1kjqnwkefn90123848976592743(*&(*&^*%&^oiusjr0928374598237,ghdomilw3;eujf npqxoi34;luwrcjto js,rhgdkcmxlas'
        res = salt.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt= res,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_dec))
        fernet_dec = Fernet(key)
    
        # opening the encrypted file
        with open(final_path, 'rb') as enc_file:
            encrypted = enc_file.read()
        
        # decrypting the file
        decrypted = fernet_dec.decrypt(encrypted)
        
        # opening the file in write mode and
        # writing the decrypted data
        with open(final_path, 'wb') as dec_file:
            dec_file.write(decrypted)

        with open(final_path,'r') as f:
            contents = f.read()
                
        byte_data = contents.encode('utf-8')

                # Create a ContentFile from byte data
        content_file = ContentFile(byte_data)


        response = FileResponse(content_file)
        response['Content-Disposition'] = f'attachment; filename="{file_path}"'
        return response
    except Exception as e:
        print(e)
        return HttpResponse("The provided encryption key is incorrect, please check the key and try again!!")

        

    
        
            
