import modules.scripts as scripts
import gradio as gr

class Script(scripts.Script):  
    # The title of the script. This is what will be displayed in the dropdown menu.
    def title(self):
        return "img2img-extras"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Group(elem_id="img2img-extras"):
            with gr.Accordion("img2img-extra", open=False):
                is_enabled = gr.Checkbox(
                    label="img2img-extra Enabled",
                    value=True,
                    elem_id="img2img-extra-enabled",
                )
                                
                img2img_keep_aspect = gr.Checkbox(False, label="Keep aspect ratio of original image and resize smaller edge to the value of 'Size'")
                smaller_edge = gr.Slider(label='Size', minimum=64, maximum=8192, step=64, value=512, visible=True, interactive=True)
                
                # pixelcount will override smaller edge if both are enabled
                img2img_pixelcount_ar = gr.Checkbox(True, label="Keep aspect ratio of original image and resize to 'Pixelcount")
                pixelcount = gr.Number(label="Pixelcount", minimum=256*256, value=640*640)

                return [is_enabled,img2img_keep_aspect,smaller_edge,img2img_pixelcount_ar,pixelcount]

    def process(self, p, 
                    is_enabled, img2img_keep_aspect, smaller_edge, img2img_pixelcount_ar, pixelcount
                    ):
        
        if not is_enabled: return p

        img = p.init_images[0] # initial image
        
        width = p.width
        height = p.height

        # rescale to fixed size of smaller edge
        if img2img_keep_aspect:
            if img.width < img.height:
                ar = img.height/img.width # aspect ratio

                width  = int(smaller_edge)
                height = int(smaller_edge * ar)
            else:
                ar = img.width/img.height # aspect ratio

                width  = int(smaller_edge * ar)
                height = int(smaller_edge)

        # rescale to a certain pixel count
        if img2img_pixelcount_ar:
            width = img.width
            height = img.height
            # reduce resolution until pixelcount is reached
            while width*height >= pixelcount:
                width  *= 0.999
                height *= 0.999

            # increase resolution until pixelcount is reached
            while width*height < pixelcount: 
                width  *= 1.001
                height *= 1.001

        width = int(width)
        height = int(height)

        p.width = width 
        p.height = height 
