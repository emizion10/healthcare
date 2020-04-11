from . models import *
from . forms import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render_to_response, redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from . decorators import *
from django.urls import reverse
from django.db.models import Q


@login_required(login_url='login')
def home(request):

    if request.user.user_type == 1:
        pt = get_object_or_404(Patient, username=request.user)
        follow = Follow.objects.filter(
            patient__username=request.user).values_list('following', flat=True)
        post = Post.objects.filter(author__in=follow)

    elif request.user.user_type == 2:
        pt = get_object_or_404(Doctor, username=request.user)
        follow = Follow.objects.filter(
            doctor__username=request.user).values_list('following', flat=True)
        post = Post.objects.filter(author__in=follow)

    else:
        post = Post.objects.filter()

    return render(request, 'pages/home.html', {'posts': post})


def index(request):
    return render(request, 'pages/index.html')


def capture(request):
    return render(request, 'pages/capture2.html')


class MyPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            user_test_result = self.get_test_func()()
            if not request.user.is_authenticated or not user_test_result:
                return HttpResponse('<h2> Permission Denied ! </h2>')
            return super().dispatch(request, *args, **kwargs)


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('/home/')

    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("/home/")

    else:
        form = UserAuthenticationForm()

    context['login_form'] = form

    return render(request, "registration/login.html", {'form': form})


class AddPatient(MyPermissionMixin, CreateView):

    raise_exception = True
    login_url = "/login/"
    model = MyUser
    template_name = 'pages/addpatient.html'
    form_class = PatientForm
    success_url = '/home/'

    def test_func(self):
        return (self.request.user.user_type == 2)

    def form_valid(self, form):
        usr = form.save(commit=False)
        username = form.cleaned_data['username']
        pname = form.cleaned_data['pname']
        gender = form.cleaned_data['gender']
        dob = form.cleaned_data['dob']
        age = form.cleaned_data['age']
        height = form.cleaned_data['height']
        weight = form.cleaned_data['weight']
        bloodgroup = form.cleaned_data['bloodgroup']
        place = form.cleaned_data['place']
        imagefile = self.request.FILES['imagefile']
        password = form.cleaned_data['password']
        usr.set_password(password)
        usr.user_type = 1
        usr.save()

        Patient.objects.create(username=usr, pname=pname, gender=gender, dob=dob, age=age,
                               height=height, weight=weight, bloodgroup=bloodgroup, place=place, imagefile=imagefile)

        return super(AddPatient, self).form_valid(form)


class AddDoctor(MyPermissionMixin, CreateView):
    raise_exception = True
    login_url = "/login/"
    model = MyUser
    template_name = 'pages/adddoctor.html'
    form_class = DoctorForm
    success_url = '/home/'

    def test_func(self):
        return (self.request.user.user_type == 3)

    def form_valid(self, form):
        doc = form.save(commit=False)
        username = form.cleaned_data['us']

        imagefile = self.request.FILES['imagefile'] if 'imagefile' in self.request.FILES else False
        if imagefile == False:
            imagefile = 'default.jpg'
        password = form.cleaned_data['password']

        usr = MyUser.objects.create()
        usr.username = username
        usr.set_password(password)
        usr.user_type = 2
        usr.save()
        doc.username = usr
        doc.save()

        return super(AddDoctor, self).form_valid(form)


class DoctorProfile(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'doctor'

    def get_object(self):
        return get_object_or_404(Doctor, username=self.request.user)

    template_name = 'pages/doctorprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 2)


class PatientProfile(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'patient'

    def get_object(self):
        return get_object_or_404(Patient, username=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(PatientProfile, self).get_context_data(**kwargs)
        pt = get_object_or_404(Patient, username=self.request.user)
        context['records'] = MedicalRecord.objects.filter(patient_id=pt)
        return context

    template_name = 'pages/patientprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 1)


class HospitalProfile(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'hospital'

    def get_object(self):
        return get_object_or_404(Hospital, username=self.request.user)

    template_name = 'pages/hospitalprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 3)


class MC(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'patient'

    def get_object(self):
        return get_object_or_404(Patient, username=self.request.user)

    template_name = 'pages/mc.html'

    def test_func(self):
        return (self.request.user.user_type == 1)



class TreatPatient(MyPermissionMixin, TemplateView):
    raise_exception = True
    login_url = "/login/"

    template_name = 'pages/treatpatient.html'

    def test_func(self):
        return (self.request.user.user_type == 2)


@user_is_doctor
def treatpatientprofile(request):
    if request.method == 'POST':
        request.session['regid'] = request.POST['regid']
        reg = request.POST['regid']
        pt = get_object_or_404(Patient, regid=reg)
        doc = get_object_or_404(Doctor, username=request.user)

        rec = MedicalRecord.objects.filter(Q(permission='public') | Q(
            doctor_id=doc) | Q(access__iregex=r'('+str(doc.dname)+'),?'))
        return render(request, 'pages/patientprofile.html', {'patient': pt, 'records': rec})


@user_is_doctor
def addmedicalrecord(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medrecord = form.save(commit=False)
            medrecord.permission = 'private'
            medrecord.doctor_id = get_object_or_404(
                Doctor, username=request.user)
            medrecord.patient_id = get_object_or_404(
                Patient, regid=request.session['regid'])
            medrecord.save()
            pt = get_object_or_404(Patient, regid=request.session['regid'])
            doc = get_object_or_404(Doctor, username=request.user)
            rec = MedicalRecord.objects.filter(Q(permission='public') | Q(
                doctor_id=doc) | Q(access__iregex=r'('+str(doc.dname)+'),?'))
            return render(request, 'pages/patientprofile.html', {'patient': pt, 'records': rec})
    else:
        form = MedicalRecordForm()

    return render(request, 'pages/addmedicalrecord.html', {'forms': form})


class MedicalRecordDetail(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    model = MedicalRecord
    context_object_name = 'record'

    template_name = 'pages/medicalrecord.html'

    def test_func(self):
        return (self.request.user.user_type == 2 or self.request.user.user_type == 1)


@user_is_patient
def editpermission(request):
    id = request.GET.get('id')
    perm = request.GET.get('type')
    custom = request.GET.get('custom')
    medrec = get_object_or_404(MedicalRecord, id=id)
    medrec.permission = perm
    if perm == 'custom':
        medrec.access = custom
    else:
        medrec.access = ''
    medrec.save()
    return HttpResponse('success')


class ViewDoctor(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'doctor'

    def get_object(self, *args, **kwargs):
        self.request.session['doctor'] = self.kwargs['slug']
        return get_object_or_404(Doctor, dname=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ViewDoctor, self).get_context_data(**kwargs)
        if self.request.user.user_type == 1:
            pt = get_object_or_404(Patient, username=self.request.user)
        elif self.request.user.user_type == 2:
            pt = get_object_or_404(Doctor, username=self.request.user)

        doc = get_object_or_404(Doctor, dname=self.kwargs['slug'])
        followers = pt.follower.filter(following=doc)
        if followers:
            context['follow'] = 'True'
        else:
            context['follow'] = 'False'

        return context

    template_name = 'pages/doctorprofile.html'

    def test_func(self):
        return (self.request.user.user_type == 1 or self.request.user.user_type == 2)


class DoctorList(MyPermissionMixin, ListView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'doctor'

    def get_queryset(self):
        if self.request.user.user_type == 1:
            pt = get_object_or_404(Patient, username=self.request.user)
            follow = Follow.objects.filter(
                patient__username=self.request.user).values_list('following', flat=True)

        elif self.request.user.user_type == 2:
            pt = get_object_or_404(Doctor, username=self.request.user)
            follow = Follow.objects.filter(
                doctor__username=self.request.user).values_list('following', flat=True)

        return Doctor.objects.filter(id__in=follow)

    def get_context_data(self, **kwargs):
        context = super(DoctorList, self).get_context_data(**kwargs)
        if self.request.user.user_type == 1:
            pt = get_object_or_404(Patient, username=self.request.user)
            follow = Follow.objects.filter(
                patient__username=self.request.user).values_list('following', flat=True)

        elif self.request.user.user_type == 2:
            pt = get_object_or_404(Doctor, username=self.request.user)
            follow = Follow.objects.filter(
                doctor__username=self.request.user).values_list('following', flat=True)

        context['unfollow'] = Doctor.objects.filter().exclude(
            id__in=follow).exclude(username=self.request.user)

        return context

    template_name = 'pages/doctorlist.html'

    def test_func(self):
        return (self.request.user.user_type == 1 or self.request.user.user_type == 2)


@login_required(login_url='login')
def sendmessage(request):
    reciever = request.GET.get('reciever')
    subject = request.GET.get('subject')
    content = request.GET.get('content')
    typemsg = request.GET.get('type')
    
    rec = get_object_or_404(MyUser, username=reciever)
    Messages.objects.create(sender=request.user,
                            reciever=rec, subject=subject, content=content)
    doc = get_object_or_404(Doctor, username=rec)

    if typemsg=='reply':
        return HttpResponseRedirect(reverse('viewmessage'))
    else:    
        return HttpResponseRedirect(reverse('viewdoctor', args=(doc.dname,)))

@login_required(login_url='login')
def deletemessage(request,**kwargs):
    msg = get_object_or_404(Messages,id=kwargs['pk'])
    if (msg.sender == request.user or msg.reciever==request.user):
        msg.delete()
    return HttpResponseRedirect(reverse('viewmessage'))




class ViewMessage(MyPermissionMixin, ListView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'message'

    def get_queryset(self):

        return Messages.objects.filter(reciever=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ViewMessage, self).get_context_data(**kwargs)
        
        context['send_message'] = Messages.objects.filter(sender=self.request.user) 
        return context

    template_name = 'pages/messages.html'

    def test_func(self):
        return (self.request.user.user_type == 1 or self.request.user.user_type == 2)




@login_required(login_url='login')
def followdoctor(request, **kwargs):

    if request.user.user_type == 1:
        pt = get_object_or_404(Patient, username=request.user)
    elif request.user.user_type == 2:
        pt = get_object_or_404(Doctor, username=request.user)

    doc = get_object_or_404(Doctor, id=kwargs['pk'])
    Follow.objects.create(following=doc, follower=pt)
    return HttpResponseRedirect(reverse('viewdoctor', args=(doc.dname,)))

@login_required(login_url='login')
def unfollowdoctor(request, **kwargs):
    doc = get_object_or_404(Doctor, id=kwargs['pk'])
    if request.user.user_type == 1:
        pt = get_object_or_404(Patient, username=request.user)
        follow = Follow.objects.get(
            following=doc, patient__username=request.user)
    elif request.user.user_type == 2:
        pt = get_object_or_404(Doctor, username=request.user)
        follow = Follow.objects.get(
            following=doc, doctor__username=request.user)

    follow.delete()
    return HttpResponseRedirect(reverse('viewdoctor', args=(doc.dname,)))


@user_is_patient
def addreview(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor = get_object_or_404(
                Doctor, dname=request.session['doctor'])
            review.author = get_object_or_404(
                Patient, username=request.user)
            review.save()
            doc = get_object_or_404(Doctor, dname=request.session['doctor'])
            return render(request, 'pages/doctorprofile.html', {'doctor': doc, })
    else:
        form = ReviewForm()

    return render(request, 'pages/doctorreview.html', {'form': form})


class DoctorPosts(MyPermissionMixin, ListView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'posts'

    def get_queryset(self):
        dt = get_object_or_404(Doctor, username=self.request.user)
        queryset = Post.objects.filter(author=dt)
        return queryset

    template_name = 'pages/myposts.html'

    def test_func(self):
        return (self.request.user.user_type == 2)


@user_is_doctor
def addpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = get_object_or_404(
                Doctor, username=request.user)
            post.save()
            dt = get_object_or_404(Doctor, username=request.user)
            pt = Post.objects.filter(author=dt)
            return render(request, 'pages/myposts.html', {'posts': pt, })
    else:
        form = PostForm()

    return render(request, 'pages/addpost.html', {'form': form})


class PostDetail(MyPermissionMixin, DetailView):
    raise_exception = True
    login_url = "/login/"
    context_object_name = 'post'
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        pre = Preference.objects.filter(
            user=self.request.user).filter(post=self.kwargs['pk'])
        if pre:
            context['preference'] = get_object_or_404(
                Preference, post=post, user=self.request.user)

        context['comments'] = Comments.objects.filter(post=post)
        return context

    template_name = 'pages/postdetail.html'

    def test_func(self):
        return (self.request.user.user_type == 1 or self.request.user.user_type == 2)


@login_required(login_url='login')
def postpreference(request, **kwargs):
    post = get_object_or_404(Post, id=kwargs['pk'])

    pre = Preference.objects.filter(
        user=request.user).filter(post=kwargs['pk'])
    if pre:
        pref = get_object_or_404(Preference, user=request.user, post=post)
        if kwargs['value'] == 1:
            post.likes = post.likes + 1
            post.dislikes = post.dislikes - 1
        else:
            post.dislikes = post.dislikes + 1
            post.likes = post.likes - 1

        pref.value = kwargs['value']
        pref.save()
    else:
        if kwargs['value'] == 1:
            post.likes = post.likes + 1
        else:
            post.dislikes = post.dislikes + 1

        Preference.objects.create(
            user=request.user, post=post, value=kwargs['value'])

    pref = get_object_or_404(Preference, user=request.user, post=post)
    post.save()
    comments = Comments.objects.filter(post=post)
    return render(request, 'pages/postdetail.html', {'post': post, 'preference': pref, 'comments': comments})


@login_required(login_url='login')
def addcomment(request, **kwargs):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        post = get_object_or_404(Post, id=kwargs['pk'])
        Comments.objects.create(
            comment=comment, post=post, author=request.user)

        pre = Preference.objects.filter(
            user=request.user).filter(post=kwargs['pk'])
        if pre:
            pref = get_object_or_404(Preference, user=request.user, post=post)
        else:
            pref = {}
        comments = Comments.objects.filter(post=post)
        return render(request, 'pages/postdetail.html', {'post': post, 'preference': pref, 'comments': comments})


def logout_view(request):
    logout(request)
    return redirect("login")
