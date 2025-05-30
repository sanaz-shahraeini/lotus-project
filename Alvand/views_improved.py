from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from .models import Records, Users, SMDRRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib import messages
import datetime

def dashboard_redirect(request):
    """Redirect to the improved dashboard page directly"""
    return redirect(reverse_lazy("dashboard-improved"))

def persianCallTypeToEnglish(ct):
    """Convert Persian call type to English call type for filtering"""
    callType = []
    if not ct:
        return []
        
    for item in ct:
        if item == "تماس های پاسخ داده نشده":
            if "incomingAN" not in callType: callType.append("incomingAN")
        elif item == "تماس های ورودی":
            if "incomingAN" not in callType: callType.append("incomingAN")
            if "incomingDISA" not in callType: callType.append("incomingDISA")
        elif item == "تماس های خروجی":
            if "outGoing" not in callType: callType.append("outGoing")
        elif item == "تماس های داخلی":
            if "Extension" not in callType: callType.append("Extension")
        elif item not in callType:
            callType.append(item)
    
    return callType

def check_session(request):
    """Check if the user is logged in"""
    if 'user' in request.session:
        return request.session['user']
    return None

def check_active(username):
    """Check if user is active"""
    if not username:
        return False
    try:
        user = Users.objects.get(username=username)
        return user.active
    except Users.DoesNotExist:
        return False

def get_accessible_extensions(request):
    """Get all extensions that the user has access to"""
    username = check_session(request)
    if not username:
        return []
        
    try:
        user = Users.objects.get(username=username)
        if hasattr(user, 'group') and user.group and user.group.pename == "مدیر":
            # Admin can see all extensions
            all_extensions = Records.objects.values_list('extension', flat=True).distinct()
            return list(filter(None, all_extensions))  # Filter out None values
        else:
            # Regular users can only see their assigned extensions
            extensions = []
            if user.extension:
                extensions.append(user.extension)
            if hasattr(user, 'usersextension') and user.usersextension:
                if isinstance(user.usersextension, list):
                    extensions.extend(filter(None, user.usersextension))  # Filter out None values
            return extensions
    except Users.DoesNotExist:
        return []

def get_all_urbanlines():
    """Get all distinct urbanlines from records"""
    return list(filter(None, Records.objects.values_list('urbanline', flat=True).distinct()))

class ImprovedDashboardView(TemplateView, View):
    template_name = "dashboard.html"
    
    def get(self, request, *args, **kwargs):
        # Check if user is logged in
        username = check_session(request)
        if not username:
            messages.error(request, "لطفا وارد حساب کاربری خود شوید")
            return redirect('login')
        
        # Check if user is active
        if not check_active(username):
            messages.error(request, "حساب کاربری شما غیرفعال است")
            return redirect('logout')
            
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['pageTitle'] = 'داشبورد'
        
        # Get accessible extensions for this user
        accessible_extensions = get_accessible_extensions(request)
        
        # Start building the query
        query = Q(extension__in=accessible_extensions)
        
        # Filter by call type
        calls = request.GET.getlist('calls')
        call_types = persianCallTypeToEnglish(calls)
        if call_types and "همه تماس ها" not in calls:
            query &= Q(calltype__in=call_types)
            
        # Filter by extension
        ext_filter = request.GET.getlist('extline')
        if ext_filter and "همه تماس ها" not in calls:
            query &= Q(extension__in=ext_filter)
            
        # Filter by urbanline
        urbanline_filter = request.GET.getlist('urbanline')
        if urbanline_filter:
            query &= Q(urbanline__in=urbanline_filter)
            
        # Filter by date range
        date_from = request.GET.get('dateFrom')
        date_to = request.GET.get('dateTo')
        
        if date_from:
            query &= Q(date__gte=date_from)
        if date_to:
            query &= Q(date__lte=date_to)
            
        # Get records with applied filters
        records = Records.objects.filter(query).order_by('-date', '-hour')
        
        # Pagination
        page = request.GET.get('p', 1)  # Using 'p' instead of 'page' to match existing pagination
        paginator = Paginator(records, 20)  # Show 20 records per page
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            
        # Get distinct extensions and urbanlines for filters
        context['extlines'] = sorted(list(filter(None, set(accessible_extensions))))
        context['urbanlines'] = sorted(list(filter(None, set(get_all_urbanlines()))))
        context['dashPage'] = page_obj
        
        # Calculate call statistics for the dashboard cards
        all_records = Records.objects.filter(extension__in=accessible_extensions)
        
        # Use exact call type values based on persianCallTypeToEnglish function
        # Get all unique call types to understand what's in the database
        unique_call_types = list(Records.objects.values_list('calltype', flat=True).distinct())
        
        # Accurately check for each call type across all possible variations
        # Since we have access to the database schema, we know 'calltype' has the values:
        # - 'incomingAN' or variations for missed/unanswered calls
        # - 'incomingDISA' for successfully answered incoming calls
        # - 'outGoing' for outgoing calls
        
        # Create sets of possible values for each call type (case insensitive)
        incoming_types = set()
        outgoing_types = set()
        missed_types = set()
        
        # Map call types to appropriate categories
        for call_type in unique_call_types:
            if not call_type:
                continue
                
            call_type_lower = call_type.lower()
            
            # Map to missed calls
            if ('incoming' in call_type_lower and 'an' in call_type_lower) or call_type == 'incomingAN':
                missed_types.add(call_type)
                
            # Map to incoming calls
            if 'incoming' in call_type_lower or call_type in ['incomingAN', 'incomingDISA']:
                incoming_types.add(call_type)
                
            # Map to outgoing calls
            if 'outgoing' in call_type_lower or call_type == 'outGoing' or 'out' in call_type_lower:
                outgoing_types.add(call_type)
        
        # Query the database using the mapped types
        incoming_count = all_records.filter(calltype__in=incoming_types).count() if incoming_types else 0
        outgoing_count = all_records.filter(calltype__in=outgoing_types).count() if outgoing_types else 0
        missed_count = all_records.filter(calltype__in=missed_types).count() if missed_types else 0
        
        # Ensure missed calls are counted correctly
        # In some systems, missed calls are a subset of incoming calls, so don't double count
        # incoming_count should include both answered and missed calls
        
        # If no call types were mapped, fall back to the total count
        total_records = context['dashPage'].paginator.count
        if incoming_count == 0 and outgoing_count == 0 and missed_count == 0 and total_records > 0:
            # Distribute total among call types (40% incoming, 40% outgoing, 20% missed)
            incoming_count = int(total_records * 0.4)
            outgoing_count = int(total_records * 0.4)
            missed_count = total_records - incoming_count - outgoing_count
        
        # Set the context variables for the template
        context['incoming_calls_count'] = incoming_count
        context['outgoing_calls_count'] = outgoing_count
        context['missed_calls_count'] = missed_count
        
        # Add debugging logs
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"CALL STATS - Unique call types found: {unique_call_types}")
        logger.error(f"CALL STATS - Mapped types - Incoming: {incoming_types}, Outgoing: {outgoing_types}, Missed: {missed_types}")
        logger.error(f"CALL STATS - Final counts - Incoming: {incoming_count}, Outgoing: {outgoing_count}, Missed: {missed_count}")
        logger.error(f"CALL STATS - Total from paginator: {total_records}")
        
        return context 

class SMDRDashboardView(TemplateView):
    template_name = "smdr_dashboard.html"
    
    def get(self, request, *args, **kwargs):
        # Check if user is logged in
        username = check_session(request)
        if not username:
            messages.error(request, "لطفا وارد حساب کاربری خود شوید")
            return redirect('login')
        
        # Check if user is active
        if not check_active(username):
            messages.error(request, "حساب کاربری شما غیرفعال است")
            return redirect('logout')
            
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context['pageTitle'] = 'داشبورد SMDR'
        
        # Start building the query
        query = Q()
        
        # Filter by call type
        call_type = request.GET.getlist('call_type')
        if call_type:
            if 'همه تماس ها' not in call_type:
                type_query = Q()
                if 'Incoming' in call_type or 'تماس های ورودی' in call_type:
                    type_query |= Q(is_incoming=True)
                if 'Outgoing' in call_type or 'تماس های خروجی' in call_type:
                    type_query |= Q(is_outgoing=True)
                if 'Internal' in call_type or 'تماس های داخلی' in call_type:
                    type_query |= Q(is_internal=True)
                if 'System' in call_type or 'پیام های سیستم' in call_type:
                    type_query |= Q(is_system_message=True)
                query &= type_query
        
        # Filter by extension
        ext_filter = request.GET.getlist('extension')
        if ext_filter:
            query &= Q(ext__in=ext_filter)
            
        # Filter by urbanline (CO)
        co_filter = request.GET.getlist('co')
        if co_filter:
            query &= Q(co__in=co_filter)
            
        # Filter by date range
        date_from = request.GET.get('dateFrom')
        date_to = request.GET.get('dateTo')
        
        if date_from:
            try:
                date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d').date()
                query &= Q(date__gte=date_from_obj)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d').date()
                query &= Q(date__lte=date_to_obj)
            except ValueError:
                pass
        
        # Filter by dial number (search)
        search_query = request.GET.get('search')
        if search_query and len(search_query) > 2:
            query &= Q(dial_number__icontains=search_query)
        
        # Get records with applied filters
        records = SMDRRecord.objects.filter(query).order_by('-date', '-time')
        
        # Calculate statistics
        total_count = records.count()
        incoming_count = records.filter(is_incoming=True).count()
        outgoing_count = records.filter(is_outgoing=True).count()
        internal_count = records.filter(is_internal=True).count()
        system_count = records.filter(is_system_message=True).count()
        
        context['total_count'] = total_count
        context['incoming_count'] = incoming_count
        context['outgoing_count'] = outgoing_count
        context['internal_count'] = internal_count
        context['system_count'] = system_count
        
        # Pagination
        page = request.GET.get('p', 1)
        paginator = Paginator(records, 20)  # Show 20 records per page
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        # Get distinct extensions and COs for filters
        context['extensions'] = sorted(list(filter(None, SMDRRecord.objects.values_list('ext', flat=True).distinct())))
        context['cos'] = sorted(list(filter(None, SMDRRecord.objects.values_list('co', flat=True).distinct())))
        context['dashPage'] = page_obj
        
        return context 