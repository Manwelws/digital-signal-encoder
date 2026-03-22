import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from st_keyup import st_keyup

plt.style.use("seaborn-v0_8-darkgrid")

st.set_page_config(
    page_title="Encoder",
    page_icon=":material/transform:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About": "https://www.linkedin.com/in/manwel-wasfy-537546323/"},
)

if "calculated" not in st.session_state:
    st.session_state.calculated = False


st.title(":red[Encoding]")
st.markdown("---")


bitstream = st_keyup(
    label="Enter bit stream",
    key="bitstream",
    placeholder="010011000111",
)

wronginput = False

if bitstream and len(bitstream) > 0:
    for char in bitstream:
        if char not in ["1", "0"]:
            wronginput = True
            break

method = st.selectbox(
    "Method",
    [
        "1.NRZ-L",
        "2.NRZ-I",
        "3.Bipolar AMI",
        "4.Pseudoternary",
        "5.manchester",
        "6.Differential manchester",
        "7.B8Zs",
        "8.HDB3",
    ],
    index=0,
    key="method",
)

y = []
if wronginput:
    st.error(":material/error: bitstream should be 1's and 0's!!!!!")
elif not wronginput and len(bitstream) > 0:
    bits = [int(b) for b in bitstream]
    t = np.arange(len(bits) + 1)

    if method == "1.NRZ-L":
        for bit in bits:
            if bit == 1:
                y.append(-1)
            else:
                y.append(1)
        if len(y) > 0:
            y.append(y[-1])

    elif method == "2.NRZ-I":
        flag = -1
        for bit in bits:
            if bit == 1:
                flag *= -1

            y.append(flag)

        if len(y) > 0:
            y.append(y[-1])

    elif method == "3.Bipolar AMI":
        flag = -1
        for bit in bits:
            if bit == 1:
                flag *= -1
                y.append(flag)
            else:
                y.append(0)
        if len(y) > 0:
            y.append(y[-1])

    elif method == "4.Pseudoternary":
        flag = -1
        for bit in bits:
            if bit == 0:
                flag *= -1
                y.append(flag)
            else:
                y.append(0)
        if len(y) > 0:
            y.append(y[-1])

    elif method == "5.manchester":
        t = np.arange(0, len(bits) + 0.5, 0.5)
        for bit in bits:
            if bit == 1:
                y.append(-1)
                y.append(1)
            else:
                y.append(1)
                y.append(-1)

        if len(y) > 0:
            y.append(y[-1])

    elif method == "6.Differential manchester":
        t = np.arange(0, len(bits) + 0.5, 0.5)
        flag = -1
        for bit in bits:
            if bit == 1:
                y.append(flag)
                flag *= -1
                y.append(flag)
            else:
                flag *= -1
                y.append(flag)
                flag *= -1
                y.append(flag)

    elif method == "7.B8Zs":
        i = 0
        last_1 = -1
        while i < len(bits):
            if bits[i : i + 8] == [0, 0, 0, 0, 0, 0, 0, 0]:
                y.extend([0, 0, 0])

                y.append(last_1)

                last_1 *= -1
                y.append(last_1)

                y.append(0)

                y.append(last_1)

                last_1 *= -1
                y.append(last_1)

                i += 8

            else:
                if bits[i] == 0:
                    y.append(0)
                else:
                    last_1 *= -1
                    y.append(last_1)

                i += 1

        if len(y) > 0:
            y.append(y[-1])

    elif method == "8.HDB3":
        i = 0
        last_1 = -1
        ones_since_last_sub = 0

        while i < len(bits):
            if bits[i : i + 4] == [0, 0, 0, 0]:
                if ones_since_last_sub % 2 != 0:
                    y.extend([0, 0, 0])
                    y.append(last_1)

                else:
                    last_1 *= -1
                    y.append(last_1)
                    y.append(last_1)

                ones_since_last_sub = 0

                i += 4

            else:
                if bits[i] == 1:
                    last_1 *= -1
                    y.append(last_1)
                    ones_since_last_sub += 1
                else:
                    y.append(0)

                i += 1

        if len(y) > 0:
            y.append(y[-1])

    fig, ax = plt.subplots(figsize=[15, 3])
    ax.step(t, y, where="post", linewidth=2.5, color="red")

    # Make it look like a textbook diagram
    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks([-1, 0, 1])
    ax.set_xticks(t)
    ax.grid(True, which="both", linestyle="--", alpha=0.7)
    ax.margins(x=0)

    for i, bit in enumerate(bits):
        ax.text(i + 0.5, 1.2, str(bit), ha="center", fontweight="bold", fontsize=12)

    st.pyplot(fig)

    st.write(y)


# if "wronginput" not in st.session_state:
#     st.session_state.wronginput = False


# def checkinput():
#     st.session_state.wronginput = False
#     current_input = st.session_state.bitstream
#     for char in current_input:
#         if char not in ["0", "1"]:
#             st.session_state.wronginput = True
#             break

# bitstream = st.text_input(
#     label="Enter bit stream",
#     key="bitstream",
#     help="Enter the bits represented in 1's and 0's and not seprated by spaces ",
#     label_visibility="visible",
#     placeholder="00110001",
#     on_change=checkinput,
#     # icon="spinner",  # remeber to remove dmbhead
# )

# if st.session_state.wronginput:
#     st.error(
#         ":material/error: bitstream should be 1's and 0's!!!!!",
#     )

# if not st.session_state.wronginput and bitstream:
#     st.success(f"Valid stream accepted: {bitstream}")

# if method == "5.manchester":
#     t = np.arange(0, len(bits) + 1, 0.5)
#     biphase_y = []
#     last_bit = -1
#     cntr = -1
#     for bit in bits:
#         cntr += 1
#         if bit == 1:
#             dec = 1
#         else:
#             dec = 0

#         if cntr > 0:
#             if dec == 1:
#                 if dec == biphase_y[cntr - 2]:
#                     biphase_y.append(-1)
#                 else:
#                     biphase_y.append(1)

#             else:
#                 if dec == biphase_y[cntr - 2]:
#                     biphase_y.append(1)
#                 else:
#                     biphase_y.append(-1)
#         else:
#             biphase_y.append(1)

#         biphase_y.append(dec)
