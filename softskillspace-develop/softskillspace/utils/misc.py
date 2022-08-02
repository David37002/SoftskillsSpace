from django.forms import model_to_dict


class AvailabilityHandler:
    def __init__(self, availability):
        self.availability = availability

    def set_availability_data(self, data):
        """
        Set the availability data from the form
        """

        fields = {f.split("_")[0] for f in data.keys()}

        for field in fields:
            from_ = f"{field}_from"
            to = f"{field}_to"

            from_ = data.get(from_)
            to = data.get(to)

            if from_ and to:
                from_ = str(from_).rsplit(":", 1)[0]
                to = str(to).rsplit(":", 1)[0]

                times = f"{from_} - {to}"
                setattr(self.availability, field, times)
            else:
                setattr(self.availability, field, "")

        self.availability.save()

    def get_availability_data(self):
        """
        Return the formatted availability data as a dictionary
        """
        availability_dict = model_to_dict(self.availability)

        days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]

        times = {}
        for day in days:
            data = availability_dict.get(day) or ""
            data = data.split(" - ")

            if len(data) == 2:
                from_key = f"{day}_from"
                to_key = f"{day}_to"

                times[from_key] = data[0]
                times[to_key] = data[1]

        return times


def get_client_ip(request):
    """
    Get the current user ip address
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
