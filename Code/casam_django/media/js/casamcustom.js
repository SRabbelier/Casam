Element.addMethods({
        setWidth: function(element, width) {
                element = $(element);
                if (typeof width == "number")
                        width = width + "px";
                element.setStyle({width: width});
                return element;
        },

        setHeight: function(element, height) {
                element = $(element);
                if (typeof height == "number")
                        height = height + "px";
                element.setStyle({height: height});
                return element;
        }});