from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import QrCodes
from PIL import Image, ImageDraw
from registration.models import Profile
from django.contrib.auth.models import User
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer, 
    SquareModuleDrawer,
    RoundedModuleDrawer,
    GappedSquareModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
    
)
from django.core.files.storage import FileSystemStorage

import qrcode
import os


def render_create_qr_code_page(request):

    subscribe = 'none'
    if request.user.is_authenticated:
        username = request.user
        user_id = request.user.id
        subscribe = Profile.objects.get(user_id = user_id).subscribe
        print(username)
    else:
        username = "none"
        return redirect("/")
    
    qr_codes = QrCodes.objects.filter(user_id = username.id)

    last_qr_code = "hello"

    print(qr_codes)
    if len(qr_codes) > 0:
        last_qr_code = qr_codes[len(qr_codes) - 1]   


    user = User.objects.get(username = username)

    user_now = Profile.objects.get(user = user)

    print(user_now.subscribe)


    logotype = None
    if request.method == "POST":
        # qr_code_url to encode
        qr_code_url = request.POST.get("url")
        qr_code_name = request.POST.get("name")
        qr_code_color = request.POST.get("color")
        qr_code_back_color = request.POST.get("back_color")


        logotype = request.FILES.get("logo")  
        print("\n\n\n\n\n\n\n\n\n",logotype, "\n\n\n\n\n\n\n\n\n\n")

        file_system = FileSystemStorage()

        if logotype != None:
            logo_path = os.path.join("qr_codes", "demo", f"{username}_logo.png")
            file_system.save(name = logo_path, content= logotype)   
        if logotype == None:
            pass
            



        dots_form = request.POST.get("dots")
        eye_form = request.POST.get("eye")

        frame_around =  request.POST.get("circle")

        if qr_code_name == "":
            return redirect("/create_qr_code_page/")
               

        qr_code = qrcode.QRCode(error_correction= qrcode.constants.ERROR_CORRECT_H)
        qr_code.add_data(qr_code_url)
        qr_code.make()






        eye_drawer_module = SquareModuleDrawer()
        dots_drawer_module = SquareModuleDrawer()


        if eye_form == "circle":
            eye_drawer_module = CircleModuleDrawer()
        elif eye_form == "rounded":
            eye_drawer_module = RoundedModuleDrawer()
        elif eye_form == "gapped_square":
            eye_drawer_module = GappedSquareModuleDrawer()
        elif eye_form == "vertical_bars":
            eye_drawer_module = VerticalBarsDrawer()
        elif eye_form == "horizontal_bars":
            eye_drawer_module = HorizontalBarsDrawer()
        

        if dots_form == "circle":
            dots_drawer_module = CircleModuleDrawer(resample_method=None)
        elif dots_form == "rounded":
            dots_drawer_module = RoundedModuleDrawer()
        elif dots_form == "gapped_square":
            dots_drawer_module = GappedSquareModuleDrawer()
        elif dots_form == "vertical_bars":
            dots_drawer_module = VerticalBarsDrawer()
        elif dots_form == "horizontal_bars":
            dots_drawer_module = HorizontalBarsDrawer()



        img = qr_code.make_image(
            image_factory=StyledPilImage, 
            module_drawer= dots_drawer_module, 
            eye_drawer=eye_drawer_module, 
            
            fill_color = qr_code_color,
            back_color = qr_code_back_color).convert('RGB')
    

        if frame_around == "on":
            draw = ImageDraw.Draw(img)

            draw.ellipse(
                (0, 0, img.size[1], img.size[1]),
                fill = None,
                outline ='black',
                width=5
            )



        qrcode_names = []

        for qr_code in qr_codes:
            qrcode_names.append(qr_code.name)

        print(len(qr_codes) + 1)

        maximum_qr_codes = 0

        if user_now.subscribe == "none":
            maximum_qr_codes = 1
        elif user_now.subscribe == "standart":
            maximum_qr_codes = 10
        elif user_now.subscribe == "pro":
            maximum_qr_codes = 100




        if qr_code_name not in qrcode_names:

            if "check" not in request.POST:
                if len(qr_codes) < maximum_qr_codes:


                    if "save" in request.POST:
                        if logotype != None:
                            
                            logo = Image.open(logotype)

                            img_size = img.size[0]
                            logo = logo.resize((100, 100))

                            logo_x = (img_size - logo.size[0]) // 2
                            logo_y = (img_size - logo.size[0]) // 2
                            
                            rgba = logo.convert("RGBA")

                            img.paste(logo, (logo_x, logo_y), rgba)
                        # try:
                        img.save(os.path.abspath(__file__ + f"/../../media/qr_codes/demo/{username}_qrcode.png"))
                        QrCodes.objects.create(name = qr_code_name, image = f"/../../media/qr_codes/image/{username}/{qr_code_name}.png", user = username)
                        img.save(os.path.abspath(__file__ + f"/../../media/qr_codes/image/{username}/{qr_code_name}.png"))
                        # except:
                        #     error = "this name already used"
            else:

                print(logo_path)
                

                logo = Image.open(logotype)

                if logotype != None:

                    img_size = img.size[0]
                    logo = logo.resize((100, 100))

                    logo_x = (img_size - logo.size[0]) // 2
                    logo_y = (img_size - logo.size[0]) // 2
                    
                    rgba = logo.convert("RGBA")

                    img.paste(logo, (logo_x, logo_y), rgba)

                img.save(os.path.abspath(__file__ + f"/../../media/qr_codes/demo/{username}_qrcode.png"))

        return render(request, "create_qr_code.html", context = {"username" : username ,"qr_code_name" : logotype, "subscribe": subscribe})
    return render(request, "create_qr_code.html", context = {"username" : username, "qr_code_name" : logotype, "subscribe": subscribe})
