from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - Home Page"
        context["content"] = "BYD PC Store"
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "BYD - About us"
        context["content"] = "About us"
        context["text_on_page"] = "Some text about our company"
        return context
