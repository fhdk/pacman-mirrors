from pacman_mirrors.functions.filter_mirror_pool_functions import filter_mirror_protocols, filter_mirror_country, \
    filter_user_branch
from pacman_mirrors.functions.filter_mirror_status_functions import filter_bad_mirrors, filter_error_mirrors, \
    filter_poor_mirrors
from pacman_mirrors.functions.outputFn import write_custom_mirrors_json


def build_pool(self) -> list:
    """
    Build the pool
    :param self:
    :return:
    """

    """
    remove known bad mirrors - last sync 9999:99
    """
    work_pool = filter_bad_mirrors(mirror_pool=self.mirrors.mirror_pool)

    """
    remove known error mirrors - response time 99.99 
    """
    work_pool = filter_error_mirrors(mirror_pool=work_pool)

    """
    Apply country filter if not fasttrack which is using all mirrors from the active pool
    """
    if not self.fasttrack:
        work_pool = filter_mirror_country(mirror_pool=work_pool, country_pool=self.selected_countries)

    """
    Apply protocol filter
    """
    try:
        _ = self.config["protocols"][0]
        work_pool = filter_mirror_protocols(mirror_pool=work_pool, protocols=self.config["protocols"])
    except IndexError:
        pass

    """
    Unless the user has provided the --no-status argument we only up-to-date for system branch
    """
    if self.no_status:
        """
        Apply interval filter
        """
        if self.interval:
            work_pool = filter_poor_mirrors(mirror_pool=work_pool, interval=self.interval)
    else:
        work_pool = filter_user_branch(mirror_pool=work_pool, config=self.config)

    return work_pool
