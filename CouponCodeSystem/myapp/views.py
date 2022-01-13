from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Order, Coupon, Userprofile
from .forms import CouponForm
from datetime import date
import datetime

def index(request):
    return render(request, 'index.html')


def newcoupon(request):
    form = CouponForm()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewcoupon')
    context = {'form': form}
    return render(request, "addcoupon.html", context)


def neworder(request):
    if request.method == "POST":
        coupon = request.POST.get('coupon')
        order_amount = int(request.POST.get('order_amount'))

        c = Coupon.objects.get(promo_code=request.POST.get('coupon'))  # 'c' is object of Coupon model

        user = Userprofile.objects.filter(date_of_birth=request.user.date_of_birth).first()

        if c.discounttype == "FLAT":
            total_amount = order_amount - c.discount
        else:
            birthdate = datetime.datetime.strftime(user.date_of_birth, "%d-%m")
            today_date = datetime.date.today()
            valid_date = datetime.datetime.strftime(today_date, "%d-%m")

            if birthdate == valid_date:
                discount = order_amount * (c.discount / 100)
                total = order_amount - discount
                total_amount = total - (total * 0.1)
            else:
                discount = order_amount * (c.discount / 100)
                total_amount = order_amount - discount

        try:
            max_limit = c.max_limit
            user_limit = c.per_user_limit

            if user.is_authenticated:
                user_count = user.user_related.count()
                coupon_count = c.coupon_related.count()

                if coupon_count < max_limit:
                    if user_count >= user_limit:
                        return HttpResponse("Per user limit is over")
                    new_order = Order.objects.create(coupon=c, order_amount=order_amount,
                                                     total_amount=total_amount, user=request.user)
                    new_order.save()
                else:
                    return HttpResponse("Coupon limit is over")
        except:
            new_order = Order.objects.create(coupon=c, order_amount=order_amount,
                                             total_amount=total_amount, user=request.user)
            new_order.used += 1
            new_order.save()
        return HttpResponseRedirect('vieworder')
    else:
        return HttpResponseRedirect('index')


def vieworder(request):
    display = Order.objects.all()
    return render(request, 'display.html', {'display': display})


def viewcoupon(request):
    displaycoupon = Coupon.objects.all()
    return render(request, 'displaycoupon.html', {'displaycoupon': displaycoupon})


def editcoupon(request, pk):
    coupon = Coupon.objects.get(id=pk)
    order_count = coupon.coupon_related.filter().count()

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)

        code = request.POST.get('promo_code')
        print(code)

        if form.is_valid():
            if order_count:
                return HttpResponse("You can not change used coupon")
            else:
                coupon = code
                form.save()
                return redirect('viewcoupon')
        else:
            print(form.errors)
    else:
        form = CouponForm(instance=coupon)
    context = {'coupon': coupon, 'form': form}
    return render(request, "addcoupon.html", context)


def delcoupon(request, pk):
    coupon = Coupon.objects.get(id=pk)
    order_count = coupon.coupon_related.filter().count()

    if order_count:
        return HttpResponse("You can not delete used coupon")
    else:
        coupon.delete()
        return redirect('viewcoupon')
