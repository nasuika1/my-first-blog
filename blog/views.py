from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, UserForm
from django.shortcuts import render, get_object_or_404, redirect
from .D4DJ import DearPointCalc
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html',{'form': form})
    return render(request, 'blog/post_edit.html',{'form': form})

def dearpoint(request):
    params = {'sinaido': '', 'voltage': '', 'form': None, 'property': ''}
    if request.method == "POST":
        form = UserForm(request.POST)
        params['sinaido'] = request.POST['sinaido']
        params['voltage'] = request.POST['voltage']
        params['form'] = form
        m_info = DearPointCalc.Music(int(params['sinaido']),int(params['voltage']))
#        try:
        m_info.Main()
        pl = m_info.play_list
        property_list = []
        for i in range(len(pl)):
            property_list += [MusicProperty(pl[i][1],pl[i][2],pl[i][4],pl[i][3],pl[i][5])]
        params['property'] = property_list
#        except:
#            params['property'] = [MusicProperty('','','','','計算エラー')]
    else:
        params['form'] = UserForm()
    return render(request,'blog/dearpoint.html',params)

def home(request):
    return render(request,'blog/home.html')

class MusicProperty:
    def __init__(self,name,level,notes,getpoint,Remarks):
        self.name = name
        self.level = level
        self.notes = notes
        self.getpoint = getpoint
        self.Remarks = Remarks
