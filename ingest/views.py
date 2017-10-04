from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .models import Upload
from django.views.generic import View

from ingest.models import Repository, Content, ContentMetadata
from ingest.forms import UploadForm, SignUpForm, RepositoryForm, LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .mixins import LoginRequiredMixin

from ingest.utils import is_file_supported, is_zip, handle_zip_file


# Create your views here.

class IndexView(View):
    # return the homepage
    def get(self, request):
        # logout(request)
        return render(request, 'ingest/index.html')


# Login view
class LoginView(View):
    user = None
    form_class = LoginForm
    template_name = 'ingest/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'error': ''})

    def post(self, request, *args, **kwargs):
        # create form and populate with login data
        form = self.form_class(request.POST)
        # validate the form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate user
            self.user = authenticate(username=username, password=password)
            if self.user is not None:
                if self.user.is_active:
                    request.session.set_expiry(0)
                    login(request, self.user)
                    # set the user id in the session
                    request.session['user_id'] = self.user.id
                    return HttpResponseRedirect(reverse('ingest:maindash', args=(self.user.id,)))
                else:
                    error = 'Account locked'
            else:
                error = 'Invalid username and or password'
        else:
            error = 'Internal error please check back later'

        return render(request, self.template_name, {'error': error})


# User signup view
class SignUpView(View):
    user = None
    template_name = 'ingest/signup.html'
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        return render(request, 'ingest/signup.html')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # validate form inputs
        if form.is_valid():
            data = form.cleaned_data
            if self.pass_equal(data['password'], data['cpassword']):
                self.user = User.objects.create(
                    first_name=data['firstname'],
                    last_name=data['lastname'],
                    username=data['email'])

                # set user password and save to database
                self.user.set_password(data['password'])
                self.user.save()
                return HttpResponseRedirect(reverse('ingest:login'))
            else:
                error = 'Passwords not equal'
        else:
            error = 'There seems to be a problem with your input please check it and try again'
        return render(request, self.template_name, {'error': error})

    """
        Confirms passwords are equal
    """

    def pass_equal(self, pass_one, pass_two):
        if pass_one != pass_two:
            return False
        else:
            return True


"""
    Dashboard Views... All dashboard views
"""


class MainDashView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.id != request.session['user_id']:
            return HttpResponseRedirect(reverse('ingest:logout'))
        return render(request, 'ingest/maindash.html', {'user': request.user})


class HomeDashView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ingest/homedash.html', {'user': request.user})


class IngestDashView(LoginRequiredMixin, View):
    form = UploadForm
    model = Content
    meta = ContentMetadata
    #
    def get(self, request, *args, **kwargs):
        repo = request.user.repository_set.all()
        return render(request, 'ingest/ingestview.html', {'repo': repo})

    #
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        status = dict();

        if form.is_valid():
            repo = None

            # get the uploaded file(s)
            data = form.cleaned_data

            # Get all repositories owned by the user
            repositories = request.user.repository_set.all()

            # Make sure a valid repository is selected
            if data['title'] == 'undefined':
                return JsonResponse({'status': 'Upload error: no repository selected'})

            # We need the repository that matches the one specified by the user
            for r in repositories:
                if r.name == data['title']:
                    repo = r

            # We get the uploaded file
            file = data['content']

            # PERFORM COMPLAINCE CHECKS
            # Check file type
            if is_file_supported(file):
                status['format'] = "passed"
            else:
                status['format'] = 'failed'
                return HttpResponse(file.content_type)

            # Check if file is zip
            if is_zip(file):
                if handle_zip_file(file):
                    status['zipopend'] = "passed"
                    return HttpResponse('Files opened')
                else:
                    return HttpResponse('error opening file')

            # Extract content meta data from file
            met =  dict()
            met['type'] = file.content_type
            met['size'] = file.size
            met['tags'] = data['tags']
            met['desc'] = data['desc']

            # Strip the file extension from the file
            # content_name = f[0:f.find('.')]

            # Save the uploaded file to the specified repository
            content = self.model.objects.create(repo=repo, content_name=file.name, repo_name=data['title'], file=file, owner=request.user)
            content.save()
            content_desc = self.meta.objects.create(content=content, file_type=met['type'], file_size=met['size'],
                                         meta_tags=met['tags'], description=met['desc'])
            if content_desc:
                content_desc.save()
                return HttpResponse('meta sucessfully extracted')
            return HttpResponse('File successfully saved')
        else:
            return HttpResponse('Upload error')


# Upload(IngestView)
class StoreDashView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # get all repositories belonging to the current user
        repos = request.user.repository_set.all()
        return render(request, 'ingest/storedash.html', {'repos': repos})

    # Handle file uploads from post
    def post(self, request, *args, **kwargs):
        return render(request, '')

# Search (SearchView)
class SearchDashView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ingest/search.html')

    # Handle file uploads from post
    def post(self, request, *args, **kwargs):
        return render(request, '')

# Logout view
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('ingest:index'))


"""
    Data endpoints
"""


# create repository
class CreateRepository(LoginRequiredMixin, View):
    model = Repository
    form = RepositoryForm

    def post(self, request, *args, **kwargs):
        error = 'form error'

        # need the nuber of repositories created by the current user
        no_of_repos = len(request.user.repository_set.all())

        if no_of_repos >= 3:
            return JsonResponse({'response': 'You have reached your limit'})


        form = self.form(request.POST)
        if form.is_valid():
            repo = self.model.objects.create(owner=request.user, name=form.cleaned_data['name'])
            repo.save()
            return HttpResponse('success')
        else:
            return HttpResponse(error)



# End points
def get_repository_content(request, id):
    from ingest.models import ContentMetadata

    '''if request.is_ajax():
        if request.method == 'GET':
            repo_id = id #request.GET['repo_id']
            repo =  Repository.objects.get(pk=repo_id)
            content = list(repo.content_set.all().values('id', 'content_name'))
            data = list(content)
            response = json.dumps(data)
            return HttpResponse(response, content_type='application/json')
        else:
            return JsonResponse()'''

    if request.method == 'GET':
        repo = Repository.objects.get(pk=id)
        files = repo.content_set.all()

        meta = dict()

        for f in files:
            meta[f.content_name] = ContentMetadata.objects.get(content=f)

        return render(request, 'ingest/repository_file_list.html', {"files": files, 'repository': repo, 'meta':meta})


def get_all_users(request):
    import json
    if request.is_ajax():
        if request.method == 'GET':
            data = list(User.objects.values('first_name', 'last_name', 'username'))
            data = list(data)
            response = json.dumps(data)
            return HttpResponse(response, content_type='application/json')
    else:
        return HttpResponse('Endpoint service link breakage')


