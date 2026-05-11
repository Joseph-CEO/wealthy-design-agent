from datetime import datetime


class EmailTemplates:
    def __init__(self, sender_name: str, frontend_url: str = "http://localhost:3000"):
        self.sender_name = sender_name
        self.frontend_url = frontend_url
        self.year = datetime.now().year

    def intro(self, client_name: str | None, project_title: str) -> str:
        name = client_name or "there"
        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
<div style="text-align:center;padding:30px 0;">
  <h1 style="color:#2d2d2d;margin:0;">{self.sender_name}</h1>
  <p style="color:#666;font-size:14px;">Graphic Designer — Nairobi</p>
</div>
<hr style="border:none;border-top:1px solid #eee;">
<p>Hi {name},</p>
<p>I came across your project: <strong>"{project_title}"</strong> and I believe my skills
as a professional graphic designer align perfectly with what you're looking for.</p>
<p>I specialize in:</p>
<ul>
  <li>Logo Design & Brand Identity</li>
  <li>Book Layouts & Covers</li>
  <li>Packaging Design</li>
  <li>Signboards, Flyers, Posters, Menus & Banners</li>
  <li>Website Design</li>
</ul>
<p>You can view my portfolio here:
<a href="{self.frontend_url}/portfolio" style="color:#007bff;">{self.frontend_url}/portfolio</a></p>
<p>I'd love to discuss how I can bring your vision to life. Would you be available for
a quick chat this week?</p>
<p>Best regards,<br><strong>{self.sender_name}</strong><br>
Nairobi, Kenya<br>
<a href="{self.frontend_url}/contact" style="color:#007bff;">Get a Quote</a></p>
<hr style="border:none;border-top:1px solid #eee;">
<p style="color:#999;font-size:12px;text-align:center;">
  &copy; {self.year} {self.sender_name}. All rights reserved.</p>
</body>
</html>"""

    def follow_up(self, client_name: str | None, project_title: str) -> str:
        name = client_name or "there"
        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
<div style="text-align:center;padding:20px 0;">
  <h2 style="color:#2d2d2d;margin:0;">Quick Follow-Up</h2>
</div>
<hr style="border:none;border-top:1px solid #eee;">
<p>Hi {name},</p>
<p>I just wanted to follow up on my previous message about your project:
<strong>"{project_title}"</strong>.</p>
<p>I'm currently accepting new projects and would be excited to help bring your
vision to life. Here's a quick overview of what I can offer:</p>
<ul>
  <li><strong>Free consultation</strong> — Let's discuss your ideas</li>
  <li><strong>Competitive pricing</strong> — Quality design within your budget</li>
  <li><strong>Fast turnaround</strong> — Most projects completed within 5-7 days</li>
  <li><strong>Unlimited revisions</strong> — Until you're 100% satisfied</li>
</ul>
<p>View my full portfolio:
<a href="{self.frontend_url}/portfolio" style="color:#007bff;">{self.frontend_url}/portfolio</a></p>
<p>Simply reply to this email or visit
<a href="{self.frontend_url}/contact" style="color:#007bff;">my contact page</a>
to get started.</p>
<p>Looking forward to hearing from you!</p>
<p>Best regards,<br><strong>{self.sender_name}</strong></p>
<hr style="border:none;border-top:1px solid #eee;">
<p style="color:#999;font-size:12px;text-align:center;">
  &copy; {self.year} {self.sender_name}. All rights reserved.</p>
</body>
</html>"""

    def proposal(self, client_name: str | None, project_title: str, amount: float) -> str:
        name = client_name or "there"
        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
<div style="text-align:center;padding:20px 0;">
  <h2 style="color:#2d2d2d;margin:0;">Design Proposal</h2>
</div>
<hr style="border:none;border-top:1px solid #eee;">
<p>Hi {name},</p>
<p>Thank you for discussing your project <strong>"{project_title}"</strong> with me.
Based on our conversation, I've prepared the following proposal:</p>
<table style="width:100%;border-collapse:collapse;margin:20px 0;">
  <tr>
    <td style="padding:10px;border:1px solid #ddd;"><strong>Project</strong></td>
    <td style="padding:10px;border:1px solid #ddd;">{project_title}</td>
  </tr>
  <tr>
    <td style="padding:10px;border:1px solid #ddd;"><strong>Total</strong></td>
    <td style="padding:10px;border:1px solid #ddd;"><strong>${amount:.2f} USD</strong></td>
  </tr>
  <tr>
    <td style="padding:10px;border:1px solid #ddd;"><strong>Timeline</strong></td>
    <td style="padding:10px;border:1px solid #ddd;">5-7 business days</td>
  </tr>
  <tr>
    <td style="padding:10px;border:1px solid #ddd;"><strong>Revisions</strong></td>
    <td style="padding:10px;border:1px solid #ddd;">Unlimited until satisfaction</td>
  </tr>
</table>
<p>To proceed, please confirm via reply and I'll send a secure payment link.</p>
<p>Best regards,<br><strong>{self.sender_name}</strong></p>
</body>
</html>"""

    def delivery(self, client_name: str | None, project_title: str) -> str:
        name = client_name or "there"
        return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
<div style="text-align:center;padding:20px 0;">
  <h2 style="color:#2d2d2d;margin:0;">Your Designs Are Ready!</h2>
</div>
<hr style="border:none;border-top:1px solid #eee;">
<p>Hi {name},</p>
<p>I'm excited to share the final designs for <strong>"{project_title}"</strong>!</p>
<p style="text-align:center;padding:20px;">
  <a href="{self.frontend_url}/client/login"
     style="background:#007bff;color:white;padding:12px 30px;text-decoration:none;border-radius:5px;">
    View Your Designs
  </a>
</p>
<p>Once you're happy with everything, you can complete payment securely
via the link below:</p>
<p style="text-align:center;padding:10px;">
  <a href="{self.frontend_url}/payment" style="color:#007bff;">Pay Online</a>
  &nbsp;|&nbsp; We accept: Visa, Mastercard, M-Pesa, PayPal
</p>
<p>It's been a pleasure working with you. If you need any changes, just let me know!</p>
<p>Best regards,<br><strong>{self.sender_name}</strong></p>
<hr style="border:none;border-top:1px solid #eee;">
<p style="color:#999;font-size:12px;text-align:center;">
  &copy; {self.year} {self.sender_name}. All rights reserved.</p>
</body>
</html>"""

    def plain_text_intro(self, client_name: str | None, project_title: str) -> str:
        name = client_name or "there"
        return f"""Hi {name},

I came across your project: "{project_title}" and I believe my skills as a professional graphic designer align perfectly with what you're looking for.

I specialize in:
- Logo Design & Brand Identity
- Book Layouts & Covers
- Packaging Design
- Signboards, Flyers, Posters, Menus & Banners
- Website Design

View my portfolio: {self.frontend_url}/portfolio
Get a quote: {self.frontend_url}/contact

I'd love to discuss how I can bring your vision to life.

Best regards,
{self.sender_name}
Nairobi, Kenya"""

    @staticmethod
    def subject(project_title: str, template_type: str = "intro") -> str:
        subjects = {
            "intro": f"Graphic Designer for: {project_title}",
            "follow_up": f"Following up — {project_title}",
            "proposal": f"Proposal for: {project_title}",
            "delivery": f"Your designs are ready — {project_title}",
        }
        return subjects.get(template_type, f"Regarding: {project_title}")
