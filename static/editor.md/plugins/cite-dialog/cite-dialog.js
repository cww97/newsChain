/*!
 * Cite dialog plugin for Editor.md
 *
 * @file        cite-dialog.js
 * @author      cww97
 * @version     0.0
 * @updateTime  2018-08-09
 */

(function () {

    var factory = function (exports) {

        var pluginName = "cite-dialog";

        exports.fn.citeDialog = function (event) {

            var _this = this;
            var cm = this.cm;
            var editor = this.editor;
            var settings = this.settings;
            var selection = cm.getSelection();
            var lang = this.lang;
            var classPrefix = this.classPrefix;
            var dialogName = classPrefix + pluginName, dialog;
            var label_str = "权&nbsp;重&nbsp;(-10&nbsp;to&nbsp;+10):";

            var citeMethod = function (event, cite_type) {
                var vote   = dialog.find("select").val();
                //var vote = dialog.find("[data-vote]").val();
                if (!vote) vote = 0;
                if (vote > 10) vote = 10;
                if (vote < -10) vote = -10;
                var cursor = cm.getCursor();
                var attr = ("{name=cite cite=" + cite_type + " vote=" + vote + "}");
                cm.replaceSelection(selection + event.copy + attr);
                if (selection === "") {
                    //console.log(event[copy]);
                    cm.setCursor(cursor.line, cursor.ch + event.copy.length);
                }
                dialog.hide().lockScreen(false).hideMask();
                return false;
            };

            cm.focus();

            if (editor.find("." + dialogName).length > 0) {
                dialog = editor.find("." + dialogName);
                dialog.find("[data-vote]").val("");

                this.dialogShowMask(dialog);
                this.dialogLockScreen();
                dialog.show();
            } else {

                var dialogHTML = "<div class=\"" + classPrefix + "form\">" +
                    event.preview +
                    "<label>" + "<strong>选择态度</strong>" + "</label>" +
                    "<select>"+
                    "<option value='1'> 支持</option>>"+
                    "<option selected='selected' value='0'>" + "无态度" + "</option>" +
                    "<option value='-1'> 反对</option>>"+
                    "</select><br/></div>";
                    /*
                    "<div class=\"" + classPrefix + "form\">" +
                    "<label>" + label_str + "</label>" +
                    "<input type=\"text\" value=\"\" data-vote />" +
                    "<br/></div>";
                     */


                dialog = this.createDialog({
                    title: "添加引用",
                    width: 380,
                    height: (event.has_img)? 505: 365,
                    content: dialogHTML,
                    mask: settings.dialogShowMask,
                    drag: settings.dialogDraggable,
                    lockScreen: settings.dialogLockScreen,
                    maskStyle: {
                        opacity: settings.dialogMaskOpacity,
                        backgroundColor: settings.dialogMaskBgColor
                    },
                    buttons: {
                        cite: ["Cite", function () {
                            return citeMethod(event, "cite");
                        }],
                        /*
                        derive: ["Derive", function () {
                            return citeMethod(event, "derive");
                        }],*/
                        cancel: [lang.buttons.cancel, function () {
                            this.hide().lockScreen(false).hideMask();
                            return false;
                        }]
                    }
                });
            }
        };
    };

    // CommonJS/Node.js
    if (typeof require === "function" && typeof exports === "object" && typeof module === "object") {
        module.exports = factory;
    } else if (typeof define === "function") {  // AMD/CMD/Sea.js
        if (define.amd) { // for Require.js
            define(["editormd"], function (editormd) {
                factory(editormd);
            });
        } else { // for Sea.js
            define(function (require) {
                var editormd = require("./../../editormd");
                factory(editormd);
            });
        }
    } else {
        factory(window.editormd);
    }
})();
