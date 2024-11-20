from django.shortcuts import HttpResponse,redirect,render,get_object_or_404
from .models import Business,Feedback,TextQuestions,RateQuestions,FeedbackForm
from .forms import ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from .forms import userloginForm,UserSignUpForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import csv
import json
from blog.models import User
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# from django.utils import timezone

@login_required
def business(request):
    businesses = Business.objects.all()
    feedbacks = Feedback.objects.all().order_by('-created_at')
    text_questions = TextQuestions.objects.all()
    rate_questions = RateQuestions.objects.all()

    total_rating = 0
    valid_feedbacks = 0
    for feedback in feedbacks:
        try:
            rating = int(feedback.rating.split(':')[-1].strip())
            total_rating += rating
            valid_feedbacks += 1
            feedback.star_range = range(rating)
            feedback.empty_star_range = range(5 - rating)
        except ValueError:
            pass

    avg_rating = round(total_rating / valid_feedbacks, 1) if valid_feedbacks else 0
    avg_rating_range = range(int(avg_rating))
    avg_rating_empty_range = range(5 - int(avg_rating))

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('business')
    else:
        form = ProfileForm() 

    context = {
        'businesses': businesses, 
        'feedbacks': feedbacks, 
        'form': form,
        'text_questions': text_questions,
        'rate_questions': rate_questions,
        'avg_rating': avg_rating,
        'avg_rating_range': avg_rating_range,
        'avg_rating_empty_range': avg_rating_empty_range,
    }
    return render(request, 'business.html', context)


# @login_required
# def download_feedbacks_csv(request):
#     feedbacks = Feedback.objects.all().order_by('-created_at')
    
#     response = HttpResponse(content_type='text/csv;')
#     response['Content-Disposition'] = 'attachment; filename="feedbacks.csv"'
    
#     writer = csv.writer(response)
#     writer.writerow(['Name','Text', 'Rating' ,'Email','Phone No.','status','Created At'])  # Header row

#     for feedback in feedbacks:
#         writer.writerow([
#             feedback.name,
#             feedback.text,
#             feedback.rating,
#             feedback.email,
#             feedback.phone_number,
#             feedback.status,
#             feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
#         ])
    
#     return response

@login_required
def download_feedbacks_csv(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # Get all unique text and rating questions
    text_questions = TextQuestions.objects.values_list('text', flat=True).distinct()
    rating_questions = RateQuestions.objects.values_list('rating', flat=True).distinct()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedbacks.csv"'
    
    writer = csv.writer(response)
    
    # Create header row with basic fields + all questions
    header = [
        'Name', 
        'Email',
        'Phone No.',
        'Status',
        'Created At',
        
    ]
    
    # Add text questions to header
    header.extend([f'Question: {q}' for q in text_questions])
    
    # Add rating questions to header
    header.extend([f'Rating: {q}' for q in rating_questions])
    
    writer.writerow(header)
    
    # Write data rows
    for feedback in feedbacks:
        # Parse text responses into a dictionary
        text_responses = {}
        if feedback.text:
            for line in feedback.text.split('\n'):
                if ':' in line:
                    question, answer = line.split(':', 1)
                    text_responses[question.strip()] = answer.strip()
        
        # Parse rating responses into a dictionary
        rating_responses = {}
        if feedback.rating:
            for line in feedback.rating.split('\n'):
                if ':' in line:
                    question, rating = line.split(':', 1)
                    rating_responses[question.strip()] = rating.strip()
        
        # Create row with basic data
        row = [
        
            feedback.name,
            feedback.email,
            feedback.phone_number,
            feedback.status,
            feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ]
        
        # Add text question responses
        for question in text_questions:
            row.append(text_responses.get(question, ''))
        
        # Add rating question responses
        for question in rating_questions:
            row.append(rating_responses.get(question, ''))
        
        writer.writerow(row)
    
    return response


def addform(request):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    businesses = Business.objects.all()
    questions = TextQuestions.objects.all() 
    ratings = RateQuestions.objects.all() 
    
    # form_type = FeedbackForm.objects.filter(name="form_type").order_by('-created_at').first()  
    # form_type_id = form_type.id if form_type else None

    if request.method == "POST":
        action = request.POST.get("action")
        print(action, "fasdjkhfjksadhfk")

        if action == "add-question":
            question = request.POST.get('question')
            form_type = request.POST.get('formName')
            form_id = None
            if form_type:
                is_exist = FeedbackForm.objects.filter(name=form_type)
                print('is_existis_existis_exist',is_exist)
                if not is_exist.exists():
                   is_exist = FeedbackForm.objects.create(business=businesses.first(), name=form_type)
                else:
                    is_exist = is_exist.last()
                form_id = is_exist
                print('form_idform_idform_id',form_id)

            print("Received question:", form_type)
            # if question:
            #     try:
            #         TextQuestions.objects.create(text=question,form_type=form_id)
            #         return JsonResponse({"Status": True, 'message': "Question added successfully"})
            #     except Exception as e:
            #         print(f"Database error: {e}")
            #         return JsonResponse({"Status": False, 'message': "Error adding question"})
            # else:
            #     print("Question cannot be empty")
            #     return JsonResponse({"Status": False, 'message': "Question cannot be empty"})

            if question:
                try:
                    new_question = TextQuestions.objects.create(text=question, form_type=form_id)
                    return JsonResponse({
                    "Status": True, 
                    'message': "Question added successfully",
                    'question': new_question.text,  # Add the new question text
                    'id': new_question.id,            # Add the new question id for future reference
                })
                except Exception as e:
                    print(f"Database error: {e}")
                return JsonResponse({"Status": False, 'message': "Error adding question"})
            else:
                return JsonResponse({"Status": False, 'message': "Question cannot be empty"})

        elif action == "add-rating":
            rating = request.POST.get('rating')
            form_type = request.POST.get('formName')
            form_id = None
            if form_type:
                is_exist = FeedbackForm.objects.filter(name=form_type)
                print('is_existis_existis_exist',is_exist)
                if not is_exist.exists():
                   is_exist = FeedbackForm.objects.create(business=businesses.first(), name=form_type)
                else:
                    is_exist = is_exist.last()
                form_id = is_exist
                print('form_idform_idform_id',form_id)
            print('ratingrating',rating)

            if rating: 
                new_rating = RateQuestions.objects.create(rating=rating, form_type=form_id)
                return JsonResponse({
                "Status": True, 
                'message': "Rating added successfully",
                'rating': new_rating.rating,  # Add the new rating text
                'id': new_rating.id,           # Add the new rating id for future reference
            })
            else:
                return JsonResponse({"Status": False, 'message': "Rating cannot be empty"})
        
        elif action == "submit-form":
            form_type = request.POST.get('formName')
            status = request.POST.get('formType')
            questions = json.loads(request.POST.get('questions', '[]'))
            ratings = json.loads(request.POST.get('ratings', '[]'))
            print('ratingsratings',ratings)
            business = Business.objects.all().order_by('-created_at').first()
            business_id = business.id if business else None

            feedback_form = FeedbackForm.objects.create(
            name=form_type,
            status=status,
            business_id=business_id
            )

            for question in questions:
                TextQuestions.objects.create(text=question, form_type=feedback_form)

            for rating in ratings:
                RateQuestions.objects.create(rating=rating, form_type=feedback_form)


            return JsonResponse({"Status": True, 'message': "Form submitted successfully"})

    context = {
        'businesses': businesses,
        'questions': questions,
        'ratings': ratings,
        # 'business_id': business_id,
        # 'form_type_id': form_type_id,
    }    

    return render(request, 'addforms.html', context)



# def team(request):
#    return HttpResponse("teammmmmmm")

@login_required
def setupformdetails(request,form_type):
    print(request.POST, "Received POST data")
    # form_type = request.GET.get('formName') 
    # print('form_typeform_typeform_typeform_type',form_type)
    businesses = Business.objects.all()
    form = None
    if form_type:
        print('form_typeform_typeform_type',form_type)
        form = FeedbackForm.objects.filter(name=form_type).first()
        questions = TextQuestions.objects.filter(form_type__name=form_type).order_by('-created_at')
        print('questionsques,tionsquestionsquestions',questions)
        ratings = RateQuestions.objects.filter(form_type__name=form_type).order_by('-created_at')
        print('ratingsratiratingsngsratingsratingsratings',ratings)
    else:
        questions = TextQuestions.objects.none()  # No questions if no form type
        ratings = RateQuestions.objects.none() 

    # questions = TextQuestions.objects.filter(form_type=form_type).order_by('-created_at')
    # ratings = RateQuestions.objects.filter(form_type=form_type).order_by('-created_at')

    # businesses = Business.objects.all()
    # questions = TextQuestions.objects.all().order_by('-created_at')
    # ratings = RateQuestions.objects.all().order_by('-created_at')
    
    
    if request.method == "POST":
        action = request.POST.get("action")
        print(action, '>>>>>>>>>>>>>>>>')

        if action == "add-question":
            question = request.POST.get('question')
            print('questionquestionquestion',question)
            # form_type = request.POST.get('form_type')
            # status = request.POST.get('status')

            if question and form: 
                print('questionquestionquestionquestion',question)
                print('formformformform',form)
                # Create the question and store form_type and status
                TextQuestions.objects.create(text=question, form_type=form)
                return JsonResponse({"Status": True, 'message': "Question added successfully"})
            else:
                if not question:
                    return JsonResponse({"Status": False, 'message': "Question cannot be empty"})
                if not form:
                    return JsonResponse({"Status": False, 'message': "Form type is invalid"})

        elif action == "add-rating":
            rating = request.POST.get('rating')
            # form_type = request.POST.get('form_type')

            print(rating, '>>>>>>>>>>>>>>>>')

            if rating and form: 
                RateQuestions.objects.create(rating=rating,form_type=form)
                return JsonResponse({"Status": True, 'message': "Rating added successfully"})
            else:
                return JsonResponse({"Status": False, 'message': "Rating cannot be empty"})
            
        elif action == "delete-question":
            question_id = request.POST.get('question_id') 

            try:
                question = TextQuestions.objects.get(id=question_id) 
                question.delete()
                return JsonResponse({"Status": True, 'message': "Question deleted successfully"})
            except TextQuestions.DoesNotExist:
                return JsonResponse({"Status": False, 'message': "Question does not exist"})

        elif action == "delete-rating":
            rating_id = request.POST.get('rating_id') 
            try:
                rating = RateQuestions.objects.get(id=rating_id) 
                print(">>>>>>>>>>>>>>>>rating",rating)
                rating.delete() 
                print(">>>>>>>>>>>>>delterating",rating)
                return JsonResponse({"Status": True, 'message': "Rating deleted successfully"})
            except RateQuestions.DoesNotExist:
                return JsonResponse({"Status": False, 'message': "Rating does not exist"})
            
        elif action == "edit-question":
            question_id = request.POST.get('question_id') 
            print('question_idquestion_idquestion_id',question_id)
            new_text = request.POST.get('new_text') 
            print('new_textnew_textnew_textnew_text',new_text)

            try:
                question = TextQuestions.objects.get(id=question_id) 
                print('questionquestionquestionquestion',question)
                question.text = new_text 
                question.save() 
                return JsonResponse({"Status": True, 'message': "Question updated successfully"})
            except TextQuestions.DoesNotExist:
                return JsonResponse({"Status": False, 'message': "Question does not exist"})
            except Exception as e:
                return JsonResponse({"Status": False, 'message': str(e)})
            

        elif action == "edit-rating":
            rating_id = request.POST.get('rating_id') 
            print('rating_idrating_idrating_id',rating_id)
            new_rating = request.POST.get('new_rating') 
            print('new_ratingnew_ratingnew_rating',new_rating)

            try:
                rating = RateQuestions.objects.get(id=rating_id) 
                print('ratingratingrating',rating)
                rating.rating = new_rating 
                rating.save() 
                return JsonResponse({"Status": True, 'message': "Rating updated successfully"})
            except RateQuestions.DoesNotExist:
                return JsonResponse({"Status": False, 'message': "Rating does not exist"})
            except Exception as e:
                return JsonResponse({"Status": False, 'message': str(e)})


    return render(request, 'setupfeedbackformdetail.html', {
        'businesses': businesses,
        'questions': questions,
        'ratings': ratings,
        'form_type': form_type,
        'form': form
    })

def setupform(request):
    if request.method == 'POST':
        form_id = request.POST.get('form_id')
        form = get_object_or_404(FeedbackForm, id=form_id)
        # Toggle status
        form.status = "Inactive" if form.status == "Active" else "Active"
        form.save()
        return redirect('setup_feedback_form') 

    # Get all feedback forms
    feedback_forms = FeedbackForm.objects.all()
    businesses = Business.objects.all()

    forms_data = []
    for form in feedback_forms:
        text_questions_count = TextQuestions.objects.filter(form_type=form.id).count()
        ratings_count = RateQuestions.objects.filter(form_type=form.id).count()
        
        forms_data.append({
            'id': form.id,
            'name': form.name,
            'text_questions_count': text_questions_count,
            'ratings_count': ratings_count,
            'status': form.status,
            'created_at': form.created_at
        })

    context = {
        'forms_data': forms_data,
        'businesses': businesses,
    }
    return render(request, 'setupfeedbackform.html', context)



def userSignUpViews(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password) 
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username,password, "password>>>>>>>>>>>>>>>>>")
        user = authenticate(username=username, password=password)
        # print(user, "user>>>>>>>>>>>>>>>>>>>>>>>>>")
        if user is not None:   
            login(request,user=user)
            messages.success(request,"You are now logged in as {username}")
            return redirect("business")
    form = userloginForm()
    return render(request, "login.html", {"form": form,})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login') 


def customer_feedback(request, business_id, form_id,form_type):
    business = get_object_or_404(Business, id=business_id)
    form = get_object_or_404(FeedbackForm, id=form_id, business=business,status='Active')
    text_questions = TextQuestions.objects.filter(form_type=form.id)
    rate_questions = RateQuestions.objects.filter(form_type=form.id)
    businesses = Business.objects.all()
    # form_type = request.Get.get('form_type')
    # form_name = Feedback.objects.get(form_type=form_type)
    
    feedback = Feedback(
        business=business, 
        form_type=form,
        name='',
        email='',
        phone_number='',
        text='', 
        rating='' 
    )

    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        form_id = request.POST.get('form_id')
        # form_type = request.POST.get('formName', form_type)
        feedback.name = request.POST.get('username')
        feedback.phone_number = request.POST.get('phone')
        feedback.email = request.POST.get('email')

        for question in text_questions:
            answer = request.POST.get(f'text_question_{question.id}')
            if answer:
                feedback.text += f"{question.text}: {answer}\n"                           #1
        
        for question in rate_questions:
            rating = request.POST.get(f'rate_question_{question.id}')
            if rating:
                feedback.rating += f"{question.rating}: {rating}\n"


        # for question in text_questions:
        #     answer = request.POST.get('text_question_' + str(question.id))
        # if answer:
        #     feedback.text += question.text + ': ' + answer + '\n'

        # for question in rate_questions:
        #     rating = request.POST.get('rate_question_' + str(question.id))                2
        # if rating:
        #     feedback.rating += str(question.rating) + ': ' + rating + '\n'

        # feedback_dict = {
        #     'text': [],
        #     'rating': []
        # }

        # for question in text_questions:
        #     answer = request.POST.get(f'text_question_{question.id}')
        #     if answer:
        #         feedback_dict['text'].append(f"{question.text}: {answer}")

        # for question in rate_questions:
        #     rating = request.POST.get(f'rate_question_{question.id}')                                      #3
        #     if rating:
        #         feedback_dict['rating'].append(f"{question.rating}: {rating}")

        # feedback.text += '\n'.join(feedback_dict['text']) + '\n'
        # feedback.rating += '\n'.join(feedback_dict['rating']) + '\n'

        # feedback_dict = {
        #     'text': [],
        #     'rating': []
        # }

        # for question in text_questions:
        #     answer = request.POST.get('text_question_' + str(question.id))
        #     if answer:
        #         feedback_dict['text'].append(question.text + ': ' + answer + '\n')

        # for question in rate_questions:
        #     rating = request.POST.get('rate_question_' + str(question.id))                                      #3
        #     if rating:
        #         feedback_dict['rating'].append(str(question.rating) + ': ' + rating + '\n')

        # feedback.text += '\n'.join(feedback_dict['text']) + '\n'
        # feedback.rating += '\n'.join(feedback_dict['rating']) + '\n'
    
        feedback.save()
        return JsonResponse({'status': 'success'})
    
    context = {
        'text_questions': text_questions,
        'rate_questions': rate_questions,
        'business': business,
        'form': form,
        'businesses': businesses,
        # 'form_type': form_type,
    }

    return render(request, 'customer_feedback.html', context)


from django.core.mail import send_mail
from django.conf import settings

def send_email(request):
    subject = "share your feedback"
    html_message = """
    <html>
      <body>
        <p>I hope you like it. Please share your review with us.</p>
        <p><a href='http://127.0.0.1:8000/customer_feedback/business/1/form/58/Dining'>Click here</a></p>
      </body>
    </html>
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["yoyoyo0011@yopmail.com"]

    if subject and html_message and from_email:
        try:
            # Sending the email
            send_mail(
                    subject, 
                    message="",
                    html_message=html_message,
                    recipient_list=recipient_list,
                    from_email=from_email,
                )
       
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        return HttpResponse("Your mail has been sent to the user")
    else:
        return HttpResponse("Make sure all fields are entered and valid.")



# @csrf_exempt
# def add_team_member(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             email = data.get('email')
#             first_name = data.get('first_name')
#             last_name = data.get('last_name')
            
#             # Create new user with unusable password
#             user = User.objects.create(
#                 username=email,
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name,
#                 is_active=False  # Set initially inactive
#             )
#             user.set_unusable_password()
#             user.save()

#             # Add user to the business team
#             business = Business.objects.get(teamMember=request.user)
#             business.teamMember.add(user)

#             # Generate token for password creation
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
            
#             # Create password set link
#             password_set_link = request.build_absolute_uri(
#                 reverse('create_password', kwargs={'uidb64': uid, 'token': token})
#             )

#             # Send welcome email with password creation link
#             subject = 'Welcome to Our Team - Set Your Password'
#             message = f'''Hello {first_name},

# Welcome to our team! To complete your account setup, please create your password by clicking the link below:


# {password_set_link}

# This link will expire in 24 hours for security purposes.

# Best regards,
# The Team'''

#             try:
#                 send_mail(
#                     subject,
#                     message,
#                     settings.DEFAULT_FROM_EMAIL,
#                     [email],
#                     fail_silently=False,
#                 )
#             except Exception as e:
#                 print(f"Error sending email: {str(e)}")

#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Team member added successfully'
#             })

#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': str(e)
#             }, status=400)

#     return JsonResponse({
#         'status': 'error',
#         'message': 'Invalid request method'
#     }, status=405)

# def create_password(request, uidb64, token):
#     try:
#         # Decode the user ID
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             password = request.POST.get('password')
#             confirm_password = request.POST.get('confirm_password')

#             if password and password == confirm_password:
#                 # Set the password and activate the user
#                 user.set_password(password)
#                 user.is_active = True
                
#                 # Update user status to Active
#                 try:
#                     # Try to update the status field if it exists
#                     user.status = 'Active'
#                 except AttributeError:
#                     # If status field doesn't exist, we'll skip it
#                     pass
                
#                 user.save()
                
#                 # Update status in Business model if the user is a team member
#                 try:
#                     business = Business.objects.get(teamMember=user)
#                     if business:
#                         # Ensure the business knows this team member is active
#                         business.save()
#                 except Business.DoesNotExist:
#                     pass
                
#                 messages.success(request, 'Password set successfully. You can now login.')
#                 return redirect('login')
#             else:
#                 messages.error(request, 'Passwords do not match.')
        
#         return render(request, 'create_password.html')
#     else:
#         messages.error(request, 'Invalid or expired password reset link.')
#         return redirect('login')

# @login_required
# def team(request):
#     # Get the business associated with the current user
#     businesses = Business.objects.all()
#     business = get_object_or_404(Business, teamMember=request.user)
#     # Get all team members for this business
#     team_members = business.teamMember.all()
    
#     context = {
#         'team_members': team_members,
#         'businesses': businesses,
#     }
#     return render(request, 'team_members.html', context)


# @login_required
# @csrf_exempt
# def delete_team_member(request, member_id):
#     if request.method == 'POST':
#         try:
#             # Get the business and ensure the current user has permission
#             business = get_object_or_404(Business, teamMember=request.user)
#             member = get_object_or_404(User, id=member_id)
            
#             # Ensure the member belongs to the business and is not the owner
#             if member not in business.teamMember.all() or member == request.user:
#                 return JsonResponse({
#                     'status': 'error',
#                     'message': 'Unauthorized access'
#                 }, status=403)
            
#             # Remove member from business and delete user account
#             business.teamMember.remove(member)
#             member.delete()
            
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Team member deleted successfully'
#             })
            
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': str(e)
#             }, status=400)
    
#     return JsonResponse({
#         'status': 'error',
#         'message': 'Invalid request method'
#     }, status=405)


# @login_required
# @csrf_exempt
# def update_team_member(request, member_id):
#     if request.method == 'POST':
#         try:
#             # Get the business and ensure the current user has permission
#             business = get_object_or_404(Business, teamMember=request.user)
#             member = get_object_or_404(User, id=member_id)
            
#             # Ensure the member belongs to the business and is not the owner
#             if member not in business.teamMember.all() or member == request.user:
#                 return JsonResponse({
#                     'status': 'error',
#                     'message': 'Unauthorized access'
#                 }, status=403)
            
#             # Parse the request data
#             data = json.loads(request.body)
            
#             # Update member information
#             member.email = data.get('email')
#             member.username = data.get('email')  # If using email as username
#             member.first_name = data.get('first_name')
#             member.last_name = data.get('last_name')
#             member.save()
            
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Team member updated successfully'
#             })
            
#         except Exception as e:
#             return JsonResponse({
#                 'status': 'error',
#                 'message': str(e)
#             }, status=400)
    
#     return JsonResponse({
#         'status': 'error',
#         'message': 'Invalid request method'
#     }, status=405)

@csrf_exempt
@login_required
def manage_team_member(request, member_id=None):
    business = get_object_or_404(Business, teamMember=request.user)
    print("ddddddddddddddddddddddddddddddddddddddddddddddddd",request.method)
    if request.method == 'POST':
        try:
            if member_id:  # Update or delete
                print(member_id,'member_idmember_idmember_id')

                member = get_object_or_404(User, id=member_id)
                print(member,'<><><><><><><><><><><>')
                if member not in business.teamMember.all() or member == request.user:
                    return JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=403)

                data = {}  # Initialize data to an empty dictionary

                try:
                    data = json.loads(request.body)
                    print('Data:', data)
                except json.JSONDecodeError as e:
                    print('JSON Decode Error:', e)
                    print('Raw Body:', request.body.decode('utf-8'))
                    return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)  # Return an error response

                if data.get('action') == 'delete':
                    print("Deleting team member...")
                    business.teamMember.remove(member)  # Ensure 'member' is defined
                    member.delete()
                    return JsonResponse({'status': 'success', 'message': 'Team member deleted successfully'})

                # Update member information
                member.email = data.get('email')
                member.username = data.get('email')
                member.first_name = data.get('first_name')
                member.last_name = data.get('last_name')
                member.save()
                return JsonResponse({'status': 'success', 'message': 'Team member updated successfully'})

            else:  # Add new member
                data = json.loads(request.body)
                email = data.get('email')
                first_name = data.get('first_name')
                last_name = data.get('last_name')

                user = User.objects.create(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=False
                )
                user.set_unusable_password()
                user.save()

                business.teamMember.add(user)

                # Generate token for password creation
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                # Create password set link
                password_set_link = request.build_absolute_uri(
                    reverse('create_password', kwargs={'uidb64': uid, 'token': token})
                )


                # Send welcome email
                subject = 'Welcome to Our Team - Set Your Password'
                message = f'Hello {first_name},\n\nWelcome to our team! To complete your account setup, please create your password by clicking the link below:\n\n{password_set_link}\n\nThis link will expire in 24 hours for security purposes.\n\nBest regards,\nThe Team'

                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

                return JsonResponse({'status': 'success', 'message': 'Team member added successfully'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# @login_required
def team(request):
    businesses = Business.objects.all()
    business = get_object_or_404(Business, teamMember=request.user)
    team_members = business.teamMember.all()
    context = {'team_members': team_members,'businesses':businesses}
    return render(request, 'team_members.html', context)


# def create_password(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)

#         if default_token_generator.check_token(user, token):
#             if request.method == 'POST':
#                 password = request.POST.get('password')
#                 user.set_password(password)
#                 user.is_active = True  # Activate the user after setting the password
#                 user.save()
#                 messages.success(request, 'Your password has been set successfully. You can now log in.')
#                 return redirect('login')  # Redirect to your login page

#             return render(request, 'create_password.html', {'user': user})

#         else:
#             messages.error(request, 'Invalid token or expired link.')
#             return redirect('home')  # Redirect to your home page

#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         messages.error(request, 'Invalid link.')
#         return redirect('home')  # Redirect to your home page
    

    
def create_password(request, uidb64, token):
    try:
        # Decode the user ID
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password and password == confirm_password:
                # Set the password and activate the user
                user.set_password(password)
                user.is_active = True
                
                # Update user status to Active
                try:
                    # Try to update the status field if it exists
                    user.status = 'Active'
                except AttributeError:
                    # If status field doesn't exist, we'll skip it
                    pass
                
                user.save()
                
                # Update status in Business model if the user is a team member
                try:
                    business = Business.objects.get(teamMember=user)
                    if business:
                        # Ensure the business knows this team member is active
                        business.save()
                except Business.DoesNotExist:
                    pass
                
                messages.success(request, 'Password set successfully. You can now login.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
        
        return render(request, 'create_password.html')
    else:
        messages.error(request, 'Invalid or expired password reset link.')
        return redirect('login')

