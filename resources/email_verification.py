from flask_restful import Resource, reqparse
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import get_current_user, jwt_required
from models import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

secret_key = 'rajrajhanskbrtgw490kjs!'
secret_salt = 'sixty!nine!four!twenty@'


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=secret_salt)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(
            token,
            salt=secret_salt,
            max_age=expiration
        )
    except:
        return False
    return email


def send_confirmation_mail(to_email, name, token):
    message = Mail(
        from_email=('verification@rajrajhans.com', 'Team GradGoggles'),
        to_emails=to_email,
        subject='Email Verification for GradGoggles',
        html_content='<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional //EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\r\n\r\n<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:o=\"urn:schemas-microsoft-com:office:office\" xmlns:v=\"urn:schemas-microsoft-com:vml\">\r\n<head>\r\n<!--[if gte mso 9]><xml><o:OfficeDocumentSettings><o:AllowPNG/><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml><![endif]-->\r\n<meta content=\"text/html; charset=utf-8\" http-equiv=\"Content-Type\"/>\r\n<meta content=\"width=device-width\" name=\"viewport\"/>\r\n<!--[if !mso]><!-->\r\n<meta content=\"IE=edge\" http-equiv=\"X-UA-Compatible\"/>\r\n<!--<![endif]-->\r\n<title></title>\r\n<!--[if !mso]><!-->\r\n<!--<![endif]-->\r\n<style type=\"text/css\">\r\n\t\tbody {\r\n\t\t\tmargin: 0;\r\n\t\t\tpadding: 0;\r\n\t\t}\r\n\r\n\t\ttable,\r\n\t\ttd,\r\n\t\ttr {\r\n\t\t\tvertical-align: top;\r\n\t\t\tborder-collapse: collapse;\r\n\t\t}\r\n\r\n\t\t* {\r\n\t\t\tline-height: inherit;\r\n\t\t}\r\n\r\n\t\ta[x-apple-data-detectors=true] {\r\n\t\t\tcolor: inherit !important;\r\n\t\t\ttext-decoration: none !important;\r\n\t\t}\r\n\t</style>\r\n<style id=\"media-query\" type=\"text/css\">\r\n\t\t@media (max-width: 660px) {\r\n\r\n\t\t\t.block-grid,\r\n\t\t\t.col {\r\n\t\t\t\tmin-width: 320px !important;\r\n\t\t\t\tmax-width: 100% !important;\r\n\t\t\t\tdisplay: block !important;\r\n\t\t\t}\r\n\r\n\t\t\t.block-grid {\r\n\t\t\t\twidth: 100% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.col {\r\n\t\t\t\twidth: 100% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.col>div {\r\n\t\t\t\tmargin: 0 auto;\r\n\t\t\t}\r\n\r\n\t\t\timg.fullwidth,\r\n\t\t\timg.fullwidthOnMobile {\r\n\t\t\t\tmax-width: 100% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col {\r\n\t\t\t\tmin-width: 0 !important;\r\n\t\t\t\tdisplay: table-cell !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack.two-up .col {\r\n\t\t\t\twidth: 50% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col.num4 {\r\n\t\t\t\twidth: 33% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col.num8 {\r\n\t\t\t\twidth: 66% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col.num4 {\r\n\t\t\t\twidth: 33% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col.num3 {\r\n\t\t\t\twidth: 25% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col.num6 {\r\n\t\t\t\twidth: 50% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.no-stack .col.num9 {\r\n\t\t\t\twidth: 75% !important;\r\n\t\t\t}\r\n\r\n\t\t\t.video-block {\r\n\t\t\t\tmax-width: none !important;\r\n\t\t\t}\r\n\r\n\t\t\t.mobile_hide {\r\n\t\t\t\tmin-height: 0px;\r\n\t\t\t\tmax-height: 0px;\r\n\t\t\t\tmax-width: 0px;\r\n\t\t\t\tdisplay: none;\r\n\t\t\t\toverflow: hidden;\r\n\t\t\t\tfont-size: 0px;\r\n\t\t\t}\r\n\r\n\t\t\t.desktop_hide {\r\n\t\t\t\tdisplay: block !important;\r\n\t\t\t\tmax-height: none !important;\r\n\t\t\t}\r\n\t\t}\r\n\t</style>\r\n</head>\r\n<body class=\"clean-body\" style=\"margin: 0; padding: 0; -webkit-text-size-adjust: 100%; background-color: #f8f8f9;\">\r\n<!--[if IE]><div class=\"ie-browser\"><![endif]-->\r\n<table bgcolor=\"#f8f8f9\" cellpadding=\"0\" cellspacing=\"0\" class=\"nl-container\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; min-width: 320px; Margin: 0 auto; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f8f8f9; width: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td style=\"word-break: break-word; vertical-align: top;\" valign=\"top\">\r\n<!--[if (mso)|(IE)]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td align=\"center\" style=\"background-color:#f8f8f9\"><![endif]-->\r\n<div style=\"background-color:transparent;\">\r\n<div class=\"block-grid\" style=\"Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #fff;\">\r\n<div style=\"border-collapse: collapse;display: table;width: 100%;background-color:#fff;\">\r\n<!--[if (mso)|(IE)]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"background-color:transparent;\"><tr><td align=\"center\"><table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"width:640px\"><tr class=\"layout-full-width\" style=\"background-color:#fff\"><![endif]-->\r\n<!--[if (mso)|(IE)]><td align=\"center\" width=\"640\" style=\";width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;\" valign=\"top\"><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td style=\"padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;\"><![endif]-->\r\n<div class=\"col num12\" style=\"min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;\">\r\n<div style=\"width:100% !important;\">\r\n<!--[if (!mso)&(!IE)]><!-->\r\n<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;\">\r\n<!--<![endif]-->\r\n<div align=\"center\" class=\"img-container center fixedwidth\" style=\"padding-right: 40px;padding-left: 40px;\">\r\n<!--[if mso]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr style=\"line-height:0px\"><td style=\"padding-right: 40px;padding-left: 40px;\" align=\"center\"><![endif]--><img align=\"center\" alt=\"GradGoggles\" border=\"0\" class=\"center fixedwidth\" src=\"https://assets.rajrajhans.com/gg.jpeg\" style=\"text-decoration: none; -ms-interpolation-mode: bicubic; height: auto; border: 0; width: 100%; max-width: 352px; display: block;\" title=\"GradGoggles\" width=\"352\"/>\r\n<!--[if mso]></td></tr></table><![endif]-->\r\n</div>\r\n<div style=\"color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.2;padding-top:10px;padding-right:40px;padding-bottom:10px;padding-left:40px;\">\r\n<div style=\"line-height: 1.2; font-size: 12px; color: #555555; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; mso-line-height-alt: 14px;\">\r\n<p style=\"font-size: 30px; line-height: 1.2; text-align: center; word-break: break-word; mso-line-height-alt: 36px; margin: 0;\"><span style=\"font-size: 30px; color: #2b303a;\"><strong>Activate your account</strong></span></p>\r\n</div>\r\n</div>\r\n<!--[if mso]></td></tr></table><![endif]-->\r\n<!--[if mso]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td style=\"padding-right: 40px; padding-left: 40px; padding-top: 10px; padding-bottom: 10px; font-family: Tahoma, sans-serif\"><![endif]-->\r\n<div style=\"color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.5;padding-top:10px;padding-right:40px;padding-bottom:10px;padding-left:40px;\">\r\n<div style=\"line-height: 1.5; font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; color: #555555; mso-line-height-alt: 18px;\">\r\n<p style=\"font-size: 15px; line-height: 1.5; text-align: center; word-break: break-word; font-family: inherit; mso-line-height-alt: 23px; margin: 0;\"><span style=\"color: #808389; font-size: 15px;\">Hi, ' + name + '. Click on the button below to activate your GradGoggles account</span></p>\r\n</div>\r\n</div>\r\n<!--[if mso]></td></tr></table><![endif]-->\r\n<!--[if (!mso)&(!IE)]><!-->\r\n</div>\r\n<!--<![endif]-->\r\n</div>\r\n</div>\r\n<!--[if (mso)|(IE)]></td></tr></table><![endif]-->\r\n<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->\r\n</div>\r\n</div>\r\n</div>\r\n<div style=\"background-color:transparent;\">\r\n<div class=\"block-grid\" style=\"Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #fff;\">\r\n<div style=\"border-collapse: collapse;display: table;width: 100%;background-color:#fff;\">\r\n<!--[if (mso)|(IE)]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"background-color:transparent;\"><tr><td align=\"center\"><table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"width:640px\"><tr class=\"layout-full-width\" style=\"background-color:#fff\"><![endif]-->\r\n<!--[if (mso)|(IE)]><td align=\"center\" width=\"640\" style=\";width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;\" valign=\"top\"><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td style=\"padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;\"><![endif]-->\r\n<div class=\"col num12\" style=\"min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;\">\r\n<div style=\"width:100% !important;\">\r\n<!--[if (!mso)&(!IE)]><!-->\r\n<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;\">\r\n<!--<![endif]-->\r\n<div align=\"center\" class=\"button-container\" style=\"padding-top:40px;padding-right:10px;padding-bottom:40px;padding-left:10px;\">\r\n<!--[if mso]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-spacing: 0; border-collapse: collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;\"><tr><td style=\"padding-top: 40px; padding-right: 10px; padding-bottom: 0px; padding-left: 10px\" align=\"center\"><v:roundrect xmlns:v=\"urn:schemas-microsoft-com:vml\" xmlns:w=\"urn:schemas-microsoft-com:office:word\" href=\"https://ggapi.rajrajhans.com/verify?token=' + token + '\" style=\"height:46.5pt; width:198pt; v-text-anchor:middle;\" arcsize=\"97%\" stroke=\"false\" fillcolor=\"#042f66\"><w:anchorlock/><v:textbox inset=\"0,0,0,0\"><center style=\"color:#ffffff; font-family:Tahoma, sans-serif; font-size:16px\"><![endif]--><a href=\"https://ggapi.rajrajhans.com/verify?token=' + token + '\" style=\"-webkit-text-size-adjust: none; text-decoration: none; display: inline-block; color: #ffffff; background-color: #042f66; border-radius: 60px; -webkit-border-radius: 60px; -moz-border-radius: 60px; width: auto; width: auto; border-top: 1px solid #042f66; border-right: 1px solid #042f66; border-bottom: 1px solid #042f66; border-left: 1px solid #042f66; padding-top: 15px; padding-bottom: 15px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; text-align: center; mso-border-alt: none; word-break: keep-all;\" target=\"_blank\"><span style=\"padding-left:30px;padding-right:30px;font-size:16px;display:inline-block;\"><span style=\"font-size: 16px; margin: 0; line-height: 2; word-break: break-word; mso-line-height-alt: 32px;\"><strong>Activate Account</strong></span></span></a>\r\n<!--[if mso]></center></v:textbox></v:roundrect></td></tr></table><![endif]-->\r\n</div>\r\n<!--[if (!mso)&(!IE)]><!-->\r\n</div>\r\n<!--<![endif]-->\r\n</div>\r\n</div>\r\n<!--[if (mso)|(IE)]></td></tr></table><![endif]-->\r\n<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->\r\n</div>\r\n</div>\r\n</div>\r\n<div style=\"background-color:transparent;\">\r\n<div class=\"block-grid\" style=\"Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #f8f8f9;\">\r\n<div style=\"border-collapse: collapse;display: table;width: 100%;background-color:#f8f8f9;\">\r\n<!--[if (mso)|(IE)]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"background-color:transparent;\"><tr><td align=\"center\"><table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"width:640px\"><tr class=\"layout-full-width\" style=\"background-color:#f8f8f9\"><![endif]-->\r\n<!--[if (mso)|(IE)]><td align=\"center\" width=\"640\" style=\";width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;\" valign=\"top\"><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td style=\"padding-right: 0px; padding-left: 0px; padding-top:5px; padding-bottom:5px;\"><![endif]-->\r\n<div class=\"col num12\" style=\"min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;\">\r\n<div style=\"width:100% !important;\">\r\n<!--[if (!mso)&(!IE)]><!-->\r\n<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:5px; padding-bottom:5px; padding-right: 0px; padding-left: 0px;\">\r\n<!--<![endif]-->\r\n<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"divider\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td class=\"divider_inner\" style=\"word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 20px; padding-right: 20px; padding-bottom: 20px; padding-left: 20px;\" valign=\"top\">\r\n<table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"divider_content\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 0px solid #BBBBBB; width: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td style=\"word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;\" valign=\"top\"><span></span></td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n</td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n<!--[if (!mso)&(!IE)]><!-->\r\n</div>\r\n<!--<![endif]-->\r\n</div>\r\n</div>\r\n<!--[if (mso)|(IE)]></td></tr></table><![endif]-->\r\n<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->\r\n</div>\r\n</div>\r\n</div>\r\n<div style=\"background-color:transparent;\">\r\n<div class=\"block-grid\" style=\"Margin: 0 auto; min-width: 320px; max-width: 640px; overflow-wrap: break-word; word-wrap: break-word; word-break: break-word; background-color: #2b303a;\">\r\n<div style=\"border-collapse: collapse;display: table;width: 100%;background-color:#2b303a;\">\r\n<!--[if (mso)|(IE)]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"background-color:transparent;\"><tr><td align=\"center\"><table cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"width:640px\"><tr class=\"layout-full-width\" style=\"background-color:#2b303a\"><![endif]-->\r\n<!--[if (mso)|(IE)]><td align=\"center\" width=\"640\" style=\";width:640px; border-top: 0px solid transparent; border-left: 0px solid transparent; border-bottom: 0px solid transparent; border-right: 0px solid transparent;\" valign=\"top\"><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td style=\"padding-right: 0px; padding-left: 0px; padding-top:0px; padding-bottom:0px;\"><![endif]-->\r\n<div class=\"col num12\" style=\"min-width: 320px; max-width: 640px; display: table-cell; vertical-align: top; width: 640px;\">\r\n<div style=\"width:100% !important;\">\r\n<!--[if (!mso)&(!IE)]><!-->\r\n<div style=\"border-top:0px solid transparent; border-left:0px solid transparent; border-bottom:0px solid transparent; border-right:0px solid transparent; padding-top:0px; padding-bottom:0px; padding-right: 0px; padding-left: 0px;\">\r\n<!--<![endif]-->\r\n<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"divider\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td class=\"divider_inner\" style=\"word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px;\" valign=\"top\">\r\n<table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"divider_content\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 4px solid #1AA19C; width: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td style=\"word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;\" valign=\"top\"><span></span></td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n</td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"divider\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td class=\"divider_inner\" style=\"word-break: break-word; vertical-align: top; min-width: 100%; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%; padding-top: 25px; padding-right: 40px; padding-bottom: 10px; padding-left: 40px;\" valign=\"top\">\r\n<table align=\"center\" border=\"0\" cellpadding=\"0\" cellspacing=\"0\" class=\"divider_content\" role=\"presentation\" style=\"table-layout: fixed; vertical-align: top; border-spacing: 0; border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-top: 1px solid #555961; width: 100%;\" valign=\"top\" width=\"100%\">\r\n<tbody>\r\n<tr style=\"vertical-align: top;\" valign=\"top\">\r\n<td style=\"word-break: break-word; vertical-align: top; -ms-text-size-adjust: 100%; -webkit-text-size-adjust: 100%;\" valign=\"top\"><span></span></td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n</td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n<!--[if mso]><table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\"><tr><td style=\"padding-right: 40px; padding-left: 40px; padding-top: 20px; padding-bottom: 30px; font-family: Tahoma, sans-serif\"><![endif]-->\r\n<div style=\"color:#555555;font-family:Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif;line-height:1.2;padding-top:20px;padding-right:40px;padding-bottom:30px;padding-left:40px;\">\r\n<div style=\"line-height: 1.2; font-size: 12px; font-family: Montserrat, Trebuchet MS, Lucida Grande, Lucida Sans Unicode, Lucida Sans, Tahoma, sans-serif; color: #555555; mso-line-height-alt: 14px;\">\r\n<p style=\"font-size: 12px; line-height: 1.2; word-break: break-word; text-align: left; font-family: inherit; mso-line-height-alt: 14px; margin: 0;\"><span style=\"color: #95979c; font-size: 12px;\">GradGoggles © 2020</span></p>\r\n</div>\r\n</div>\r\n<!--[if mso]></td></tr></table><![endif]-->\r\n<!--[if (!mso)&(!IE)]><!-->\r\n</div>\r\n<!--<![endif]-->\r\n</div>\r\n</div>\r\n<!--[if (mso)|(IE)]></td></tr></table><![endif]-->\r\n<!--[if (mso)|(IE)]></td></tr></table></td></tr></table><![endif]-->\r\n</div>\r\n</div>\r\n</div>\r\n<!--[if (mso)|(IE)]></td></tr></table><![endif]-->\r\n</td>\r\n</tr>\r\n</tbody>\r\n</table>\r\n<!--[if (IE)]></div><![endif]-->\r\n</body>\r\n</html>'
    )
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        if response.status_code != 200:
            return {"msg": "error in sending verification email", "reason": response.body}
    except:
        return {"msg": "error in sending verification email"}


class ConfirmUser(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', help='Token missing', required=True)
        data = parser.parse_args()

        try:
            email = confirm_token(data['token'])
            if not email:
                return {"msg": "Token Expired or Invalid"}
        except:
            return {"msg": "Token Expired or Invalid"}  # TODO: Show the User a Page

        user = User.get(User.email == email)
        if user.isVerified:
            return {"msg": "User Already Verified"}  # TODO: Show the User a Page

        User.update(
            isVerified=True
        ).where(
            User.email == email
        ).execute()

        return {"msg": "Verification Successful"}  # TODO: Show the User a Page


class ResendConfirmationEmail(Resource):
    @jwt_required
    def get(self):
        user = get_current_user()
        token = generate_confirmation_token(user.email)
        send_confirmation_mail(user.email, user.name, token)
        print("Email sent to ", user.email)


class CheckUserVerification(Resource):
    @jwt_required
    def get(self):
        user = get_current_user()
        if user.isVerified:
            return {"msg": "yes"}
        else:
            return {"msg": "no"}
