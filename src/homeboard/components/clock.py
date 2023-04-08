import fastapi

import homeboard.component
import homeboard.config

__all__ = [
    "Component",
]

HTML = """
<div id="day_info">
  <div id="clock"></div>
</div>

<script>
// Clock that is shown only within a configured window
function updateClock() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const clock = document.getElementById('clock');
    if (hours >= %s && hours < %s) {
        clock.innerHTML = `${hours}:${minutes < 10 ? '0' : ''}${minutes}`;
    } else {
        clock.innerHTML = '--:--';
    }
}
updateClock();
setInterval(updateClock, 5000);

</script>
"""


class Component(homeboard.component.Base):
    def __init__(self) -> None:
        pass

    def router(self) -> fastapi.APIRouter | None:
        return None

    def html(self) -> str:
        displayed = homeboard.config.cached().component("clock").get("displayed", {})
        begin_hour = displayed.get("begin_hour", 0)
        end_hour = displayed.get("end_hour", 24)
        return HTML % (begin_hour, end_hour)
