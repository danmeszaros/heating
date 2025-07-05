Here's the explanation in **GitHub-flavored Markdown** format, ready for a `README.md` or documentation file:

---

# 🌡️ Heating System Controller – State Machine Overview

This script manages a **temperature-controlled heating system** using a **state machine**. It monitors various sensors and controls relays to direct the flow of water between:

* A **solar collector**
* A **ground heat exchanger**
* A **boiler**

---

## 🔁 State Machine Overview

The system uses a three-state finite state machine to decide how to operate:

### **State 0 – System Off**

* System is idle.
* **Transition to State 1** if:

  * **Collector temperature** > `45°C`, or
  * **Collector outlet temperature** > `30°C`
* ✅ Starts the **collector pump**

---

### **State 1 – Ground Circulation**

* Circulates water between collector and ground loop.
* Checks:

  * 🔄 Is the system stable? (wait if not)
  * 🌡️ Is **collector or outlet temp < 20°C**? → Switch to **State 0**
  * 🔻 Is **temp difference in ground loop < 2°C**? → Switch to **State 0**
  * 🔥 Is **water to ground > 18°C**? → Switch to **State 2** (start heating boiler)

---

### **State 2 – Boiler Heating**

* Directs heat from the collector to the boiler.
* Checks:

  * 🔄 Is the system stable? If not:

    * If partially stable → **Pause**
    * Else → Wait
  * 🌡️ Is **boiler temp ≥ 57°C**? → Switch to **State 1**
  * 🔻 Is **collector outlet – boiler temp < 3°C**? → Switch to **State 1**

---

## 🧪 Sensor Inputs

| Sensor Name | Description                  |
| ----------- | ---------------------------- |
| `temp2`     | Boiler temperature           |
| `temp3`     | Collector temperature        |
| `temp5`     | Collector outlet temperature |
| `temp6`     | Water to ground loop         |
| `temp7`     | Water from ground loop       |
| `state0`    | Current system state         |

---

## ⚙️ Relay Outputs

| Relay Name | Description                   |
| ---------- | ----------------------------- |
| `relay1`   | Collector pump (or main pump) |
| `relay8`   | Boiler circulation or heating |

### 🔌 Relay Control Logic

| State | `relay1`           | `relay8` |
| ----- | ------------------ | -------- |
| **0** | OFF                | OFF      |
| **1** | ON                 | OFF      |
| **2** | ON (unless paused) | ON       |

---

## ✅ Purpose

The control logic aims to:

* Maximize energy efficiency using the **solar collector** and **ground loop**
* Avoid unnecessary heating or cooling
* Heat the **boiler** only when sufficient thermal energy is available

---

## 📋 System Stability Checks

The script uses:

```python
lib.sensor.isValueStable(config, "state0", seconds)
```

To wait until temperature readings are stable for a given time before making transitions.

---

Let me know if you'd like a flowchart, diagram, or unit tests for this system logic!

