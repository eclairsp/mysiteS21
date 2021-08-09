# Installation guide for sending email

This is the installation guide for sending email function.

In this project, the default setting is to display the email in console, not actually sending it out.

In order to enable this function, the following steps should be taken:

1. In setting.py comment out the "EMAIL_BACKEND" part [line 53](https://github.com/eclairsp/mysiteS21/blob/c68c0a9453f08ed1902234a4157645c5d98cd9ea/mysiteS21/settings.py#L53)

2. Uncomment the part after it "env = environ.Env() ... env("EMAIL_HOST_PASSWORD")" [line 56](https://github.com/eclairsp/mysiteS21/blob/c68c0a9453f08ed1902234a4157645c5d98cd9ea/mysiteS21/settings.py#L56) to [line 64](https://github.com/eclairsp/mysiteS21/blob/c68c0a9453f08ed1902234a4157645c5d98cd9ea/mysiteS21/settings.py#L64)

3. Add .env file in this directory with two parameters, EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
   * you can create your own .env file with these two parameters
   * set EMAIL_HOST_USER=yougmail@gmail.com
   * set EMAIL_HOST_PASSWORD=yourpassword
   * enable less secure access on https://support.google.com/accounts/answer/6010255?hl=en#zippy=%2Cif-less-secure-app-access-is-on-for-your-account

4. After above steps, the email can be sent but it may also appear in the spam folder.
