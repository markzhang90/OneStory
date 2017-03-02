var ImgSection = Vue.extend({
  	template: '<div class="ui divided items">' + 
                    '<div class="item">' + 
                        '<div class="content">' +
                            '<a class="header">我的标题啊</a>'+
                            '<div class="meta">' +
                                '<span class="cinema">${pickeddate}</span>' +
                                '<span class="cinema">晴</span>' +
                                '<span class="cinema"></span>' +
                            '</div>' +
                            '<div class="description">' +
                                '<p></p>' +
                            '</div>' +
                            '<div class="extra">' +
                                '<div class="ui label yellow"><i class="smile icon"></i>happy</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
  	props : ['img_data'],
})
