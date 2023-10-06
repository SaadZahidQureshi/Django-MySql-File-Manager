from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from .models import User, File
from django.contrib import messages, sessions
from app.forms import fileForm
from django.shortcuts import get_object_or_404
from mimetypes import guess_type 
# from .forms import FileSearchForm
# Create your views here.


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User()
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.password == password:
                # print("user logged in")
                request.session['email'] = user.email
                request.session['username'] = user.username
                return redirect('index')
            else:
                # print("user logged making fun")
                messages.info(request, 'Password not matching')
                return render(request, 'HTML/login.html')
    return render(request, 'HTML/login.html')

def SignUp(request):
    if request.method == 'POST':
        user = User()
        
        user.email = request.POST['email']
        user.username = user.email.split('@')[0]
        user.dob = request.POST['dob']
        user.password = request.POST['password']
        user.conf_password = request.POST['conf-password']
        if user.password == user.conf_password:
            if User.objects.filter(email=user.email).exists():
                messages.info(request, 'Email already exists')
                return render(request, 'HTML/signup.html')
            else:
                user.save()
                messages.info(request, 'User created')
                return render(request, 'HTML/signup.html')
        else:
            messages.info(request, 'Password not matching')
            return render(request, 'HTML/signup.html')

    else:
        return render(request, 'HTML/Signup.html')

def Index(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            form = fileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'File uploaded successfully.')
                return redirect('index')
            else:
                messages.error(request, 'File upload failed. Please check the form data.')
        else:
            messages.error(request, 'No file was uploaded.')
    else:
        form = fileForm()
    files = File.objects.all()
    return render(request, 'HTML/index.html', {'form': form, 'files': files, })

    # form1 = FileSearchForm(request.GET)
  
    # if form1.is_valid():
    #     search_query = form1.cleaned_data.get('search_query')
    #     if search_query:
    #         # Filter files based on the search query (customize this query as needed)
    #         files1 = files.filter(title__icontains=search_query)


    # return render(request, 'HTML/index.html',{'form': form})
    # if request.method == 'POST':

def Logout(request):
    del request.session['email']
    del request.session['username']
    return redirect('login')

def download_file(request, file_id):

    try:
        # Retrieve the file from the database
        file_obj = File.objects.get(id=file_id)
        
        # Open the file and read its content
        with file_obj.file.open('rb') as file_content:
            response = HttpResponse(file_content.read(), content_type='application/octet-stream')
        
        # Set the Content-Disposition header to prompt download
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        
        return response
    except File.DoesNotExist:
        # Handle the case where the file is not found
        return HttpResponse('File not found', status=404)
    
def view_document(request, file_id):

    try:
        # Retrieve the document from the database
        file_obj = get_object_or_404(File, id=file_id)

        # Determine the content type based on file extension
        content_type, _ = guess_type(file_obj.file.name)
        
        if content_type is None:
            content_type = 'application/octet-stream'  # Default to binary data

        # Open the document and read its content
        with file_obj.file.open('rb') as document_content:
            response = HttpResponse(document_content.read(), content_type=content_type)
        
        # Set the Content-Disposition header to prompt download
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        
        return response
    except File.DoesNotExist:
        # Handle the case where the document is not found
        return HttpResponse('Document not found', status=404)
    

def file_list(request):
    form = FileSearchForm(request.GET)
    files = File.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            # Filter files based on the search query (customize this query as needed)
            files = files.filter(title__icontains=search_query)

    return render(request, 'file_list.html', {'form': form, 'files': files})