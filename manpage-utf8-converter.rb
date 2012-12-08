#!/usr/bin/env ruby

require 'kconv'

targetfiles = []

targetfiles = Dir.glob("manual/*/man*/*")

convert_utf8 = Proc.new do
   targetfiles.length.times do |number|
      contents_orig = open(targetfiles[number], "r")
      contents_utf8 = Kconv.toutf8(contents_orig.read)

      contents_orig = open(targetfiles[number], "w")
      contents_orig.puts contents_utf8
   end
end

puts "Convert manpages (euc-jp to utf-8)..."

convert_utf8.call
