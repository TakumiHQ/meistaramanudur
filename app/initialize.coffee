# Initialize Router

class Photo extends Backbone.View
  template: (require './templates/photo')
  className: "post"
  render: =>
    ($ @el).html @template(@model.toJSON())
    return this

class InstagramView extends Backbone.View

  el: ".photos"

  initialize: (options) ->
    @collection.on "reset", @all
    @collection.on "add", @add

  add: (model) =>
    @$el.prepend (new Photo model: model).render().el

  all: =>
    # ($ @el).html ""
    @add(model) for model in @collection.models


class Meistaramanudur

  views: {}
  collections: {}

  ready: ->

    $(".sidebar ul li a[href^='#']").on 'click', (event) ->
      event.preventDefault()
      ($ 'html, body').animate
        scrollTop: ($ @hash).offset().top
      , 300

    ($ ".sidebar a").on "click", (event) ->
      $el = ($ @)
      mixpanel.track "Section",
        section: ($el.attr "href")

    ($ "form :input").on "focus", (event) ->
      $el = ($ @)
      mixpanel.track "Focus",
        field: $el.attr "name"

    ($ "#spurningar .question").each (i, el) ->
      ($ el).find("h5").on "click", (event) ->
        ($ el).addClass("open")


    submitCount = 0

    ($ "form button").button()
    ($ "form").on "submit", (event) ->
      submitCount += 1
      $form = ($ @)
      event.preventDefault()
      fields = $form.find(":input").serialize()

      $name = $form.find("[name='name']")
      $email = $form.find("[name='email']")

      unless $name.val()
        return $name.focus()
      unless $email.val()
        return $email.focus()

      mixpanel.track "Submit"
      $form.find("button").button("loading")
      $.ajax
        type: "POST"
        url: $form.attr "action"
        data: fields
        dataType: "json"
        success: (data) ->
          ($ ".thank-you").html (require './templates/thanks') count: data.number
          $form.find("button").button("done")
          mixpanel.track "Signup", {errors: submitCount - 1}
          $form.parent().addClass("done")

    @collections.instagram = new Backbone.Collection
    @views.instagram = new InstagramView collection: @collections.instagram

    hashtag = 'meistaram'
    client = 'a14c9c8243be42f2b07aed444b02edc0'

    refresh = =>
      $.ajax
        url: "https://api.instagram.com/v1/tags/#{hashtag}/media/recent?count=100&client_id=#{client}"
        dataType: "jsonp"
        success: (data, status) =>
          for photo in data.data.reverse()
            unless (@collections.instagram.get photo.id)
              @collections.instagram.add photo
    refresh()

    @pusher = new Pusher("78c7db626f8171964b75")
    channel = @pusher.subscribe("instagram")
    channel.bind "photo", (data) =>
      refresh()


$ =>
  window.meistaramanudur = new Meistaramanudur
  window.meistaramanudur.ready()
